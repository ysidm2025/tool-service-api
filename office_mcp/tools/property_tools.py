# import requests

# PROPERTY_ENDPOINT = "https://chatiqnet.rcqatol.com/25-5-0/openaibot/ai/propertysummary"
# PAYLOAD = {
#     "objecttype": "3",
#     "objectid": "510835",
#     "QueryText": "propertyinfo"
# }

# TOOL_NAMES = [
#     "pet_policy",
#     "property_email",
#     "property_number",
#     "property_reviews",
#     "apartment_availability",
#     "current_resident",
#     "office_hours",
#     "photo_gallery",
#     "maps_and_directions",
#     "apartment_amenities",
#     "community_amenities",
#     "floorplans",
# ]

# def get_property_data():
#     try:
#         response = requests.post(PROPERTY_ENDPOINT, json=PAYLOAD)
#         response.raise_for_status()
#         return response.json().get("Response", {})
#     except Exception as e:
#         return {"error": str(e)}

# # , description=f"Fetches specific property information related to '{name}'"
# def register_property_tools(mcp):
#     for tool_name in TOOL_NAMES:
#         # Define and register the tool dynamically
#         def make_tool(name):
#             @mcp.tool(name=name, description=f"Fetches specific property information related to '{name}'")
#             def tool() -> str:
#                 """Fetches specific property information."""
#                 data = get_property_data()
#                 section = data.get(name)

#                 if not section:
#                     return f"No data available for '{name}'."

#                 if isinstance(section, list):
#                     return str(section)
#                 elif isinstance(section, dict):
#                     return str(section)
#                 else:
#                     return str(section)

#             return tool

#         make_tool(tool_name)

import requests

PROPERTY_ENDPOINT = "https://chatiqnet.rcqatol.com/25-5-0/openaibot/ai/propertysummary"
PAYLOAD = {
    "objecttype": "3",
    "objectid": "510835",
    "QueryText": "propertyinfo"
}

TOOL_NAMES = [
    "pet_policy",
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


def get_property_data():
    try:
        response = requests.post(PROPERTY_ENDPOINT, json=PAYLOAD)
        response.raise_for_status()
        return response.json().get("Response", {})
    except Exception as e:
        return {"error": str(e)}


def resolve_tool_data(tool_name: str, response: dict) -> str:
    prop_info = response.get("property_info", [{}])[0]

    # Custom logic for indirect fields
    indirect_map = {
        "property_email": prop_info.get("email"),
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

    # Check top-level field by name (e.g., pet_policy, office_hours, etc.)
    section = response.get(tool_name)
    if section:
        return str(section)

    return f"No data available for '{tool_name}'."

def register_property_tools(mcp):
    for tool_name in TOOL_NAMES:
        def make_tool(name):
            @mcp.tool(name=name, description=f"Fetches specific property information related to '{name}'")
            def tool() -> str:
                """Fetches specific property information."""
                data = get_property_data()
                return resolve_tool_data(name, data)

            return tool

        make_tool(tool_name)
