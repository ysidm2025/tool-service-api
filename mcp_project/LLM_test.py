import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async def main():
    # Connect to the MCP server at /mcp/
    async with streamablehttp_client("http://localhost:8000/mcp/") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Call the "hello" tool
            result = await session.call_tool("hello", {"name": "Alice"})
            print("Result from server:", result)

            # Call a tool named "add"
            result = await session.call_tool("add", {"a": 5, "b": 7})
            print("Result:", result)
if __name__ == "__main__":
    asyncio.run(main())

# import asyncio
# from mcp.client.streamable_http import streamablehttp_client
# from mcp import ClientSession

# async def main():
#     # Connect to the MCP server at /mcp/
#     async with streamablehttp_client("http://localhost:8000") as (read, write, _):
#         async with ClientSession(read, write) as session:
#             await session.initialize()

#             # List available tools
#             tools = await session.list_tools()
#             print("Available tools:", tools)

#             # Optionally, check if "hello" tool is available before calling
#             if "hello" in tools:
#                 result = await session.call_tool("hello", {"name": "Alice"})
#                 print("Result from 'hello' tool:", result)
#             else:
#                 print("'hello' tool not found.")

#             # Uncomment below if you want to test "add" tool too
#             # if "add" in tools:
#             #     result = await session.call_tool("add", {"a": 5, "b": 7})
#             #     print("Result from 'add' tool:", result)
#             # else:
#             #     print("'add' tool not found.")

# if __name__ == "__main__":
#     asyncio.run(main())


           