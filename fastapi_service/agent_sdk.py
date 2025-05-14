# import json
# from openai import AsyncOpenAI , OpenAI # type: ignore
# from openai.types.beta.threads import MessageContent , TextContentBlock
# from utils import get_tool_metadata, get_tool_instances
# from dotenv import load_dotenv # type: ignore
# import os
# from pydantic import create_model 
# # from .metadata_loader import load_tool_descriptions
# # from openai.types.beta.threads import MessageContentTextContentBlock

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
# def answer_with_tools(query: str) -> str:
#     try:
#         tools_metadata = get_tool_metadata()
#         tool_instances = get_tool_instances()  # Should return a dict: {tool_name: tool_instance}
        
#         # Prepare OpenAI-compatible tool schemas
#         openai_tools = []
#         for tool in tools_metadata:
#             openai_tools.append({
#                 "type": "function",
#                 "function": {
#                     "name": tool["tool_name"],
#                     "description": tool["description"],
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             param: {"type": "string"} for param in tool["parameters"]
#                         },
#                         "required": tool["parameters"],
#                     },
#                 }
#             })

#         # Step 1: Create Assistant
#         assistant = client.beta.assistants.create(
#             name="Tool Agent Assistant",
#             instructions="Use tools when appropriate to solve user queries. any query by user not related to tool we have provided you reply with I can only help you with website related queries",
#             tools=openai_tools,
#             model="gpt-4-turbo"
#         )

#         # Step 2: Create Thread and Add Message
#         thread = client.beta.threads.create()
#         client.beta.threads.messages.create(
#             thread_id=thread.id,
#             role="user",
#             content=query
#         )

#         # Step 3: Run Assistant
#         run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

#         # Step 4: Poll for Tool Calls
#         while True:
#             run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
#             if run_status.status == "requires_action":
#                 tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
#                 tool_outputs = []

#                 for tool_call in tool_calls:
#                     tool_name = tool_call.function.name
#                     arguments = json.loads(tool_call.function.arguments)

#                     tool_info = tool_instances.get(tool_name)
#                     if tool_info:
#                         result = tool_info["function"](**arguments)
#                         tool_outputs.append({
#                             "tool_call_id": tool_call.id,
#                             "output": result
#                         })
#                     else:
#                         tool_outputs.append({
#                             "tool_call_id": tool_call.id,
#                             "output": f"Tool '{tool_name}' not found."
#                         })

#                 # Submit tool outputs and continue
#                 run = client.beta.threads.runs.submit_tool_outputs(
#                     thread_id=thread.id,
#                     run_id=run.id,
#                     tool_outputs=tool_outputs
#                 )
#             elif run_status.status in ["completed", "failed", "cancelled"]:
#                 break

#         # Step 5: Get Final Message
#         messages = client.beta.threads.messages.list(thread_id=thread.id)
#         last_message = messages.data[0]

#         if last_message.content and isinstance(last_message.content[0], TextContentBlock):
#             return last_message.content[0].text.value
#         else:
#             return "No meaningful response generated."

#     except Exception as e:
#         return f"Error occurred: {e}"

from openai import OpenAI
import os
import json
from utils import get_tool_metadata_from_mcp, call_mcp_tool
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def answer_with_tools(query: str) -> str:
    try:
        tools_metadata = get_tool_metadata_from_mcp()

        openai_tools = []
        for tool in tools_metadata:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool["tool_name"],
                    "description": tool["description"],
                    "parameters": {
                        "type": "object",
                        "properties": {
                            param: {"type": "string"} for param in tool["parameters"]
                        },
                        "required": tool["parameters"],
                    },
                }
            })

        assistant = client.beta.assistants.create(
            name="MCP Tool Agent",
            instructions="Use tools to answer user queries if relevant. any query by user not related to tool we have provided you reply with I can only help you with website related queries",
            tools=openai_tools,
            model="gpt-4-turbo"
        )

        thread = client.beta.threads.create()
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=query)

        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == "requires_action":
                tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []

                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    output = call_mcp_tool(tool_name, args)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": output
                    })

                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

            elif run_status.status in ["completed", "failed", "cancelled"]:
                break

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        last_message = messages.data[0]
        return last_message.content[0].text.value if last_message.content else "No response."

    except Exception as e:
        return f"Error: {e}"
