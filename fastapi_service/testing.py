from openai import OpenAI
import subprocess
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Start your MCP server
server_proc = subprocess.Popen(["dotnet", "run"], cwd="McpServer", stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# Register a tool
tool = client.beta.assistants.tools.create_tool(name="DiagnosticsTool")

# Register a tool server using stdin/stdout
tool_server = client.beta.assistants.tool_servers.register_tool_server(
    tool_id=tool.id,
    process=server_proc
)

# Ask a question that invokes the tool
run = client.beta.threads.runs.create(
    thread_id="your-thread-id",
    assistant_id="your-assistant-id",
    instructions="Check if nginx service is running"
)

print(run.output)
