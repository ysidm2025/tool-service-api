from openai import AsyncOpenAI , OpenAI # type: ignore
from openai.types.beta.threads import MessageContent , TextContentBlock
from utils import get_tool_metadata, get_tool_instances
from dotenv import load_dotenv # type: ignore
import os
from pydantic import create_model 
# from .metadata_loader import load_tool_descriptions
# from openai.types.beta.threads import MessageContentTextContentBlock

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def answer_with_tools(query: str) -> str:
#     tools_metadata = get_tool_metadata()
#     tool_instances = get_tool_instances()

#     # Convert tools to OpenAI-compatible tool schema
#     openai_tools = []
#     for tool in tools_metadata:
#         openai_tools.append(
#             {
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
#             }
#         )

#     # Create a new assistant with all tools pre-attached
#     assistant = client.beta.assistants.create(
#         name="Tool Agent Assistant",
#         instructions="Use the tools to answer questions related to maintenance, site operations, or other topics.",
#         tools=openai_tools,
#         model="gpt-4-turbo"
#     )

#     # Create a thread and add user message
#     thread = client.beta.threads.create()
#     client.beta.threads.messages.create(
#         thread_id=thread.id,
#         role="user",
#         content=query
#     )

#     # Run the assistant (DO NOT use tool_resources)
#     run = client.beta.threads.runs.create_and_poll(
#         thread_id=thread.id,
#         assistant_id=assistant.id,
#         tool_choice="auto"
#     )

#     # Get the latest message from the thread
#     messages = client.beta.threads.messages.list(thread_id=thread.id)
#     last_message = messages.data[0]

#     # Safely return the response
#     if last_message.content and isinstance(last_message.content[0], MessageContent):
#         return last_message.content[0].text.value
#     else:
#         return "No meaningful response generated."

def answer_with_tools(query: str) -> str:
    print(f"Received query: {query}")  # Debugging line
    
    # Get tool metadata and instances
    tools_metadata = get_tool_metadata()
    tool_instances = get_tool_instances()

    # Debugging: Print out loaded tool metadata
    print(f"Loaded tool metadata: {tools_metadata}")

    # Convert tools to OpenAI-compatible tool schema
    openai_tools = []
    for tool in tools_metadata:
        print(f"Processing tool: {tool['tool_name']}")  # Debugging line
        openai_tools.append(
            {
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
            }
        )

    print(f"OpenAI tools schema: {openai_tools}")  # Debugging line

    # Create a new assistant with all tools pre-attached
    try:
        assistant = client.beta.assistants.create(
            name="Tool Agent Assistant",
            instructions="Use the tools to answer questions related to maintenance, site operations, or other topics.",
            tools=openai_tools,
            model="gpt-4-turbo"
        )
        print(f"Assistant created with ID: {assistant.id}")  # Debugging line
    except Exception as e:
        print(f"Error creating assistant: {e}")
        return f"Error creating assistant: {e}"

    # Create a thread and add the user message
    try:
        thread = client.beta.threads.create()
        print(f"Thread created with ID: {thread.id}")  # Debugging line
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query
        )
    except Exception as e:
        print(f"Error creating thread or sending message: {e}")
        return f"Error creating thread or sending message: {e}"

    # Run the assistant
    try:
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            tool_choice="auto"
        )
        print(f"Assistant run completed: {run}")  # Debugging line
    except Exception as e:
        print(f"Error running assistant: {e}")
        return f"Error running assistant: {e}"

    # Get the latest message from the thread
    try:
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(f"Retrieved messages: {messages.data}")  # Debugging line
        last_message = messages.data[0]
    except Exception as e:
        print(f"Error retrieving messages: {e}")
        return f"Error retrieving messages: {e}"

    # # Safely return the response
    # if last_message.content and isinstance(last_message.content[0], MessageContent):
    #     print(f"Last message content: {last_message.content[0].text.value}")  # Debugging line
    #     return last_message.content[0].text.value
    # else:
    #     print("No meaningful response generated.")  # Debugging line
    #     return "No meaningful response generated."

    # Check if the message content exists and if the first item is a TextContentBlock (or another expected type)
    if last_message.content and isinstance(last_message.content[0], TextContentBlock):
        print(f"Last message content: {last_message.content[0].text.value}")  # Debugging line
        return last_message.content[0].text.value
    else:
        print("No meaningful response generated.")  # Debugging line
        return "No meaningful response generated."