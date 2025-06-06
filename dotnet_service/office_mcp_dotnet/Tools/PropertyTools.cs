using System.Net.Http.Json; // For sending HTTP requests with JSON content
using System.ComponentModel; // For Description attribute
using System.Text.Json; // For JSON parsing
using System.Linq; // For LINQ operations
using System.Collections.Generic; // For generic collections
using System.Threading.Tasks; // For async/await
using System.Reflection; // For reflection (not used directly here)
using ModelContextProtocol.Server; // For MCP server attributes
using System;

namespace PropertyMcpServer.Tools
{
    // Helper class to resolve property data from API responses
    public static class PropertyResolver
    {
        // Extracts a string or number property from a JsonElement as a string
        private static string GetStringOrNumberAsString(JsonElement element, string propertyName)
        {
            if (!element.TryGetProperty(propertyName, out JsonElement prop))
                return null;

            // Return the property as string or number (as string), or null if not present
            return prop.ValueKind switch
            {
                JsonValueKind.String => prop.GetString(),
                JsonValueKind.Number => prop.GetRawText(),
                JsonValueKind.Null => null,
                _ => null,
            };
        }

        // Main resolver: maps tool names to values in the API response
        public static string Resolve(string toolName, Dictionary<string, JsonElement> response)
        {
            // If response is missing or doesn't have 'property_info', handle special cases
            if (response == null || !response.TryGetValue("property_info", out var propInfo))
            {
                var keys = response?.Keys.ToList() ?? new List<string>();
                Console.WriteLine($"Debug: 'property_info' key missing in response keys: [{string.Join(", ", keys)}]");

                // Default messages for special tool names if data is missing
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
            // If property_info is an array, use the first element
            if (propInfo.ValueKind == JsonValueKind.Array)
            {
                var enumerator = propInfo.EnumerateArray();
                if (!enumerator.Any())
                    return $"No data available for '{toolName}'.";

                first = enumerator.First();
            }
            // If property_info is an object, use it directly
            else if (propInfo.ValueKind == JsonValueKind.Object)
            {
                first = propInfo;
            }
            else
            {
                return $"No data available for '{toolName}'.";
            }

            // Map tool names to values extracted from the property_info object
            var indirectMap = new Dictionary<string, string>
            {
                ["property_email"] = GetStringOrNumberAsString(first, "email"),
                ["property_name"] = GetStringOrNumberAsString(first, "name"),
                ["property_number"] = GetStringOrNumberAsString(first, "phone"),
                ["maps_and_directions"] = $"{GetStringOrNumberAsString(first, "address")}, {GetStringOrNumberAsString(first, "city")}, {GetStringOrNumberAsString(first, "state")} - Lat: {GetStringOrNumberAsString(first, "Latitude")}, Lon: {GetStringOrNumberAsString(first, "Longitude")}",

                // Default messages for these keys if not present
                ["property_reviews"] = "No reviews available in response.",
                ["apartment_availability"] = "Not directly available in API response.",
                ["current_resident"] = "Not available in response.",
                ["photo_gallery"] = "No photo gallery data in response.",

            };

            // If the requested toolName is in the indirectMap, return its value
            if (indirectMap.ContainsKey(toolName))
            {
                // For special keys, check if actual data is present in the response
                if (toolName == "property_reviews" || toolName == "apartment_availability" || toolName == "current_resident" || toolName == "photo_gallery")
                {
                    if (response.TryGetValue(toolName, out var section))
                    {
                        // Return the section as string if present
                        var sectionStr = section.ToString();
                        if (!string.IsNullOrWhiteSpace(sectionStr) && sectionStr != "null")
                            return sectionStr;
                    }
                    // Otherwise, return the default message
                    return indirectMap[toolName];
                }
                else
                {
                    // For other keys, return the value if not null
                    if (!string.IsNullOrEmpty(indirectMap[toolName]))
                        return indirectMap[toolName];
                    else
                        return $"No data available for '{toolName}'.";
                }
            }

            // If toolName is not in indirectMap, try to find it directly in the response
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

    // Main tool class for property-related MCP tools
    [McpServerToolType]
    public sealed class PropertyTools
    {
        // API endpoint for property data
        private static readonly string Endpoint = "https://chatiqnet.rcqatol.com/25-5-0/openaibot/ai/propertysummary";
        // Shared HttpClient instance
        private static readonly HttpClient client = new();

        // Fetches property data from the API using provided parameters
        private async Task<Dictionary<string, JsonElement>> FetchPropertyData(string objecttype, string objectid, string queryText)
        {
            try
            {
                // Prepare payload with default values if parameters are missing
                var payload = new Dictionary<string, string>
                {
                    ["objecttype"] = string.IsNullOrEmpty(objecttype) ? "3" : objecttype,
                    ["objectid"] = string.IsNullOrEmpty(objectid) ? "510835" : objectid,
                    ["QueryText"] = string.IsNullOrEmpty(queryText) ? "propertyinfo" : queryText
                };

                // Send POST request to the API
                var response = await client.PostAsJsonAsync(Endpoint, payload);
                response.EnsureSuccessStatusCode();

                // Read raw response as string
                var raw = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Raw API response: {raw}"); // DEBUG

                // Parse response as dictionary
                var parsed = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(raw);
                if (parsed == null)
                {
                    Console.WriteLine("Debug: Parsed response is null.");
                    return new();
                }

                // Extract inner 'Response' object if present
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

        // Calls FetchPropertyData and resolves the result for the given tool
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

        // Each method below is exposed as an MCP tool and fetches a specific property field
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
