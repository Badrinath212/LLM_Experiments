import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os


import sys

load_dotenv(override=True)

server_params = StdioServerParameters(
    command=sys.executable,
    args=["server.py"]
)

open_router_api_key = os.environ.get("OPEN_ROUTER_API_KEY")
if not open_router_api_key: 
    raise ValueError("OPEN_ROUTER_API_KEY is not set in the environment variables.")

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize connection
            await session.initialize()

            # Discover available tools
            tools = await session.list_tools()

            print("Available tools:")

            llm_tools = []

            for tool in tools.tools:
                llm_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema
                    }
                })

            llm = ChatOpenAI(
                model_name="openrouter/free",
                api_key=open_router_api_key,
                base_url="https://openrouter.ai/api/v1",
                temperature=0
            )

            llm_with_tools = llm.bind_tools(llm_tools)
            
            result = llm_with_tools.invoke("what is 10+20?")

            print("Tool result:")
            print(result.tool_calls)

            tool_call = result.tool_calls[0]

            tool_name = tool_call["name"]
            arguments = tool_call["args"]

            tool_result = await session.call_tool(
                tool_name,
                arguments=arguments
            )

            print(tool_result)


if __name__ == "__main__":
    asyncio.run(main())