import asyncio
import os
import shutil
import subprocess
import time
from typing import Any
import httpx
from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings

from dotenv import load_dotenv
load_dotenv()

async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="Use the tools to answer the questions.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    # Use the `add` tool to add two numbers
    message = "Add these numbers: 7 and 22."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_weather` tool
    message = "What's the weather in Tokyo?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_secret_word` tool
    message = "What's the secret word?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    async with MCPServerSse(
        name="SSE Python Server",
        params={
            "url": "http://localhost:8000/sse",
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="SSE Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server)


if __name__ == "__main__":
    # Let's make sure the user has uv installed
    if not shutil.which("uv"):
        raise RuntimeError(
            "uv is not installed. Please install it: https://docs.astral.sh/uv/getting-started/installation/"
        )

    # We'll run the SSE server in a subprocess. Usually this would be a remote server, but for this
    # demo, we'll run it locally at http://localhost:8000/sse
    process: subprocess.Popen[Any] | None = None

    try:
        asyncio.run(main())
    finally:
        pass

# import asyncio
# import os
# import shutil
# import subprocess
# import time
# from typing import Any

# from agents import Agent, Runner, gen_trace_id, trace
# # from agents.mcp import MCPServerHttp  # <-- Use HTTP, not SSE
# from agents.model_settings import ModelSettings
# import httpx
# from agents import Agent, Runner, gen_trace_id, trace
# from agents.mcp import MCPServer, MCPServerSse
# from agents.model_settings import ModelSettings

# from dotenv import load_dotenv
# load_dotenv()

# async def run(mcp_server):
#     agent = Agent(
#         name="Assistant",
#         instructions="Use the tools to answer the questions.",
#         mcp_servers=[mcp_server],
#         model_settings=ModelSettings(tool_choice="required"),
#     )

#     # Use the `add` tool to add two numbers
#     message = "Add these numbers: 7 and 22."
#     print(f"Running: {message}")
#     result = await Runner.run(starting_agent=agent, input=message)
#     print(result.final_output)

#     # Run the `get_weather` tool
#     message = "What's the weather in Tokyo?"
#     print(f"\n\nRunning: {message}")
#     result = await Runner.run(starting_agent=agent, input=message)
#     print(result.final_output)

#     # Run the `get_secret_word` tool
#     message = "What's the secret word?"
#     print(f"\n\nRunning: {message}")
#     result = await Runner.run(starting_agent=agent, input=message)
#     print(result.final_output)

# # async def main():
# #     async with MCPServerHttp(
# #         name="Streamable HTTP Server",
# #         params={"url": "http://localhost:8000/"},
# #     ) as server:
# #         trace_id = gen_trace_id()
# #         with trace(workflow_name="Streamable HTTP Example", trace_id=trace_id):
# #             print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
# #             await run(server)

# async def main():
#     async with MCPServerSse(
#         name="SSE Python Server",
#         params={"url": "http://localhost:8001/"},
# ) as server:
#         trace_id = gen_trace_id()
#         with trace(workflow_name="Streamable HTTP Example", trace_id=trace_id):
#             print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
#             await run(server)

# if __name__ == "__main__":
#     # Check if `uv` is installed
#     if not shutil.which("uv"):
#         raise RuntimeError(
#             "uv is not installed. Please install it: https://docs.astral.sh/uv/getting-started/installation/"
#         )

#     process: subprocess.Popen[Any] | None = None
#     try:
#         this_dir = os.path.dirname(os.path.abspath(__file__))
#         server_file = os.path.join(this_dir, "server.py")

#         print("Starting HTTP server at http://localhost:8001/ ...")
#         process = subprocess.Popen(["uv", "run", server_file])
#         time.sleep(3)
#         print("Server started. Running example...\n")
#     except Exception as e:
#         print(f"Error starting server: {e}")
#         exit(1)

#     try:
#         asyncio.run(main())
#     finally:
#         if process:
#             process.terminate()
