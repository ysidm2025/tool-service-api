from openai import AsyncOpenAI , OpenAI # type: ignore
from openai.types.beta.threads import MessageContent
from utils import get_tool_metadata, get_tool_instances
from dotenv import load_dotenv # type: ignore
import os
from pydantic import create_model 
# from .metadata_loader import load_tool_descriptions
# from openai.types.beta.threads import MessageContentTextContentBlock

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def answer_with_tools(query: str) -> str:
    tools_metadata = get_tool_metadata()
    tool_instances = get_tool_instances()

    # Convert tools to OpenAI-compatible tool schema
    openai_tools = []
    for tool in tools_metadata:
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

    # Create a new assistant with all tools pre-attached
    assistant = client.beta.assistants.create(
        name="Tool Agent Assistant",
        instructions="Use the tools to answer questions related to maintenance, site operations, or other topics.",
        tools=openai_tools,
        model="gpt-4-turbo"
    )

    # Create a thread and add user message
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=query
    )

    # Run the assistant (DO NOT use tool_resources)
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        tool_choice="auto"
    )

    # Get the latest message from the thread
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    last_message = messages.data[0]

    # Safely return the response
    if last_message.content and isinstance(last_message.content[0], MessageContent):
        return last_message.content[0].text.value
    else:
        return "No meaningful response generated."
