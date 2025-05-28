import requests
from typing import Optional

PROPERTY_ENDPOINT = "https://chatiqnet.rcqatol.com/25-5-0/openaibot/ai/propertysummary"

TOOL_NAMES = [
    "pet_policy",
    "property_name",
    "property_email",
    "property_number",
    "property_reviews",
    "apartment_availability",
    "current_resident",
    "office_hours",
    "photo_gallery",
    "maps_and_directions",
    "apartment_amenities",
    "community_amenities",
    "floorplans",
]

# Fetch property data using dynamic payload
def get_property_data(payload: dict):
    try:
        print(f"[DEBUG] Sending payload: {payload}")
        response = requests.post(PROPERTY_ENDPOINT, json=payload)
        response.raise_for_status()
        return response.json().get("Response", {})
    except Exception as e:
        return {"error": str(e)}

# Map tool name to specific section or nested logic
def resolve_tool_data(tool_name: str, response: dict) -> str:
    prop_info = response.get("property_info", [{}])[0]

    # Custom field mappings
    indirect_map = {
        "property_email": prop_info.get("email"),
        "property_name": prop_info.get("name"),
        "property_number": prop_info.get("phone"),
        "maps_and_directions": f"{prop_info.get('address', '')}, {prop_info.get('city', '')}, {prop_info.get('state', '')} - Lat: {prop_info.get('Latitude')}, Lon: {prop_info.get('Longitude')}",
        "property_reviews": "No reviews available in response.",
        "apartment_availability": "Not directly available in API response.",
        "current_resident": "Not available in response.",
        "photo_gallery": "No photo gallery data in response."
    }

    if tool_name in indirect_map:
        value = indirect_map[tool_name]
        return value if value else f"No data available for '{tool_name}'."

    section = response.get(tool_name)
    if section:
        return str(section)

    return f"No data available for '{tool_name}'."

# Register all tools with parameters
def register_property_tools(mcp):
    for tool_name in TOOL_NAMES:
        def make_tool(name):
            @mcp.tool(
                name=name,
                description=f"Fetches property info related to '{name}'",
            )
            def tool(
                objecttype: Optional[str] = "3",
                objectid: Optional[str] = "510835",
                QueryText: Optional[str] = "propertyinfo"
            ) -> str:
                # Ensure no empty values
                if not objecttype:
                    objecttype = "3"
                if not objectid:
                    objectid = "510835"
                if not QueryText:
                    QueryText = "propertyinfo"

                """Fetches property info using dynamic payload and extracts tool-specific content."""

                if not objecttype or not objectid or not QueryText:
                    return "Error: objecttype, objectid and QueryText are required parameters."
                payload = {
                    "objecttype": objecttype,
                    "objectid": objectid,
                    "QueryText": QueryText
                }

                response = get_property_data(payload)
                if "error" in response:
                    print(f"[ERROR] API returned error: {response['error']}")
                    return f"API error: {response['error']}"

                # return resolve_tool_data(name, response)
                result = resolve_tool_data(name, response)

                print(f"[DEBUG] Result for '{name}': {result}")
                return result

            return tool

        make_tool(tool_name)