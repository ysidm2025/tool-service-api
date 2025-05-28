using System.Net.Http.Json;
using System.ComponentModel;
using System.Text.Json;
using System.Linq;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Reflection;
using ModelContextProtocol.Server;
using System;

namespace PropertyMcpServer.Tools
{
    public static class PropertyResolver
    {
        private static string GetStringOrNumberAsString(JsonElement element, string propertyName)
        {
            if (!element.TryGetProperty(propertyName, out JsonElement prop))
                return null;

            return prop.ValueKind switch
            {
                JsonValueKind.String => prop.GetString(),
                JsonValueKind.Number => prop.GetRawText(),
                JsonValueKind.Null => null,
                _ => null,
            };
        }

        public static string Resolve(string toolName, Dictionary<string, JsonElement> response)
        {
            if (response == null || !response.TryGetValue("property_info", out var propInfo))
            {
                var keys = response?.Keys.ToList() ?? new List<string>();
                Console.WriteLine($"Debug: 'property_info' key missing in response keys: [{string.Join(", ", keys)}]");

                // For the special keys, return their default message if requested
                var indirectDefaultMessages = new Dictionary<string, string>
                {
                    ["property_reviews"] = "No reviews available in response.",
                    ["apartment_availability"] = "Not directly available in API response.",
                    ["current_resident"] = "Not available in response.",
                    ["photo_gallery"] = "No photo gallery data in response.",

                };

                if (indirectDefaultMessages.TryGetValue(toolName, out var defaultMsg))
                    return defaultMsg;

                return $"No data available for '{toolName}'.";
            }

            JsonElement first = default;
            if (propInfo.ValueKind == JsonValueKind.Array)
            {
                var enumerator = propInfo.EnumerateArray();
                if (!enumerator.Any())
                    return $"No data available for '{toolName}'.";

                first = enumerator.First();
            }
            else if (propInfo.ValueKind == JsonValueKind.Object)
            {
                first = propInfo;
            }
            else
            {
                return $"No data available for '{toolName}'.";
            }

            // Prepare indirect values from the first property_info element
            var indirectMap = new Dictionary<string, string>
            {
                ["property_email"] = GetStringOrNumberAsString(first, "email"),
                ["property_name"] = GetStringOrNumberAsString(first, "name"),
                ["property_number"] = GetStringOrNumberAsString(first, "phone"),
                ["maps_and_directions"] = $"{GetStringOrNumberAsString(first, "address")}, {GetStringOrNumberAsString(first, "city")}, {GetStringOrNumberAsString(first, "state")} - Lat: {GetStringOrNumberAsString(first, "Latitude")}, Lon: {GetStringOrNumberAsString(first, "Longitude")}",

                // These keys have default "not available" messages if missing
                ["property_reviews"] = "No reviews available in response.",
                ["apartment_availability"] = "Not directly available in API response.",
                ["current_resident"] = "Not available in response.",
                ["photo_gallery"] = "No photo gallery data in response.",

            };

            // --- New behavior: Check ALL keys from indirectMap, but only for requested toolName ---

            if (indirectMap.ContainsKey(toolName))
            {
                // If the indirectMap value is one of the 4 default "not available" messages, 
                // try to check if the actual response has the data (for future-proofing)
                if (toolName == "property_reviews" || toolName == "apartment_availability" || toolName == "current_resident" || toolName == "photo_gallery")
                {
                    if (response.TryGetValue(toolName, out var section))
                    {
                        // If data is present and not empty/null, return it as string
                        var sectionStr = section.ToString();
                        if (!string.IsNullOrWhiteSpace(sectionStr) && sectionStr != "null")
                            return sectionStr;
                    }
                    // Otherwise, return the default "not available" message from indirectMap
                    return indirectMap[toolName];
                }
                else
                {
                    // For other indirect keys, return the value if not null
                    if (!string.IsNullOrEmpty(indirectMap[toolName]))
                        return indirectMap[toolName];
                    else
                        return $"No data available for '{toolName}'.";
                }
            }

            // If toolName is not in indirectMap, try to find it directly in the response dictionary
            if (response.TryGetValue(toolName, out var directSection))
            {
                var directStr = directSection.ToString();
                if (!string.IsNullOrWhiteSpace(directStr) && directStr != "null")
                    return directStr;
            }

            // If nothing found, return generic message
            return $"No data available for '{toolName}'.";
        }
    }

    [McpServerToolType]
    public sealed class PropertyTools
    {
        private static readonly string Endpoint = "https://chatiqnet.rcqatol.com/25-5-0/openaibot/ai/propertysummary";
        private static readonly HttpClient client = new();

        private async Task<Dictionary<string, JsonElement>> FetchPropertyData(string objecttype, string objectid, string queryText)
        {
            try
            {
                var payload = new Dictionary<string, string>
                {
                    ["objecttype"] = string.IsNullOrEmpty(objecttype) ? "3" : objecttype,
                    ["objectid"] = string.IsNullOrEmpty(objectid) ? "510835" : objectid,
                    ["QueryText"] = string.IsNullOrEmpty(queryText) ? "propertyinfo" : queryText
                };

                var response = await client.PostAsJsonAsync(Endpoint, payload);
                response.EnsureSuccessStatusCode();

                var raw = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Raw API response: {raw}"); // DEBUG

                var parsed = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(raw);
                if (parsed == null)
                {
                    Console.WriteLine("Debug: Parsed response is null.");
                    return new();
                }

                if (parsed.TryGetValue("Response", out var responseElement))
                {
                    var innerData = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(responseElement.GetRawText());
                    if (innerData == null)
                    {
                        Console.WriteLine("Debug: Inner 'Response' data is null or invalid JSON.");
                        return new();
                    }

                    return innerData;
                }
                else
                {
                    Console.WriteLine("Debug: 'Response' key missing in parsed JSON.");
                    return new();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in FetchPropertyData: {ex}");
                return new();
            }
        }

        private async Task<string> ResolveByCaller(string toolName, string objecttype, string objectid, string queryText)
        {
            try
            {
                var data = await FetchPropertyData(objecttype, objectid, queryText);
                return PropertyResolver.Resolve(toolName, data);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in ResolveByCaller ({toolName}): {ex}");
                return $"Error resolving property data for '{toolName}'.";
            }
        }

        [McpServerTool(Name = "pet_policy"), Description("Pet policy info")]
        public Task<string> PetPolicy(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("pet_policy", objecttype, objectid, queryText);

        [McpServerTool(Name = "property_name"), Description("Property name info")]
        public Task<string> PropertyName(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("property_name", objecttype, objectid, queryText);

        [McpServerTool(Name = "property_email"), Description("Property email info")]
        public Task<string> PropertyEmail(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("property_email", objecttype, objectid, queryText);

        [McpServerTool(Name = "property_number"), Description("Property phone number")]
        public Task<string> PropertyNumber(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("property_number", objecttype, objectid, queryText);

        [McpServerTool(Name = "property_reviews"), Description("Property reviews")]
        public Task<string> PropertyReviews(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("property_reviews", objecttype, objectid, queryText);

        [McpServerTool(Name = "apartment_availability"), Description("Apartment availability info")]
        public Task<string> ApartmentAvailability(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("apartment_availability", objecttype, objectid, queryText);

        [McpServerTool(Name = "current_resident"), Description("Current resident info")]
        public Task<string> CurrentResident(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("current_resident", objecttype, objectid, queryText);

        [McpServerTool(Name = "office_hours"), Description("Office hours info")]
        public Task<string> OfficeHours(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("office_hours", objecttype, objectid, queryText);

        [McpServerTool(Name = "photo_gallery"), Description("Photo gallery info")]
        public Task<string> PhotoGallery(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("photo_gallery", objecttype, objectid, queryText);

        [McpServerTool(Name = "maps_and_directions"), Description("Maps and directions info")]
        public Task<string> MapsAndDirections(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("maps_and_directions", objecttype, objectid, queryText);

        [McpServerTool(Name = "apartment_amenities"), Description("Apartment amenities info")]
        public Task<string> ApartmentAmenities(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("apartment_amenities", objecttype, objectid, queryText);

        [McpServerTool(Name = "community_amenities"), Description("Community amenities info")]
        public Task<string> CommunityAmenities(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("community_amenities", objecttype, objectid, queryText);

        [McpServerTool(Name = "floorplans"), Description("Floorplans info")]
        public Task<string> Floorplans(string objecttype = "3", string objectid = "510835", string queryText = "propertyinfo")
            => ResolveByCaller("floorplans", objecttype, objectid, queryText);
    }
}
