import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
import sys
from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import ToolMessage

load_dotenv(override=True)

server_params = StdioServerParameters(
    command=sys.executable,
    args=["server.py"]
)

llm_tools = []

open_router_api_key = os.environ.get("OPEN_ROUTER_API_KEY")
if not open_router_api_key: 
    raise ValueError("OPEN_ROUTER_API_KEY is not set in the environment variables.")

class AgentState(TypedDict):
    messages: list[Any]

def call_llm(state: AgentState):

    llm = ChatOpenAI(
        model_name="openrouter/free",
        api_key=open_router_api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0
    )

    llm_with_tools = llm.bind_tools(llm_tools)

    response = llm_with_tools.invoke(state["messages"])
    
    return {"messages": state["messages"] + [response]}

def route_node(state: AgentState):
    last_message = state["messages"][-1]

    if  last_message.tool_calls:
        print("MCP Tool Call:", last_message.tool_calls[0])
        return "call_mcp_tool"
    print("LLM Response:", last_message.content)
    return "exit"

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize connection
            await session.initialize()

            async def call_mcp_tool(state: AgentState):
                last_message = state["messages"][-1]

                tool_call = last_message.tool_calls[0]

                tool_name = tool_call["name"]
                arguments = tool_call["args"]

                tool_result = await session.call_tool(
                    tool_name,
                    arguments=arguments
                )

                print("MCP Tool Result:", tool_result)

                tool_message = ToolMessage(
                    content=str(tool_result.structured_content),
                    tool_call_id=tool_call["id"]
                )

                return {
                    "messages": state["messages"] + [tool_message]
                }

            # Discover available tools
            tools = await session.list_tools()

            print("Available tools:")

            for tool in tools.tools:
                llm_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema
                    }
                })
                print(f"- {tool.name}: {tool.description}")

            graph = StateGraph(AgentState)

            graph.add_node("call_llm", call_llm)
            graph.add_node("call_mcp_tool", call_mcp_tool)

            graph.add_edge(START, "call_llm")
            graph.add_conditional_edges(
                "call_llm",
                route_node,
                {
                    "call_mcp_tool": "call_mcp_tool",
                    "exit": END
                }
            )
            graph.add_edge("call_mcp_tool", END)

            app = graph.compile()

            result = await app.ainvoke({
                "messages": [
                    {"role": "user", "content": "what is 100+150?"}
                ]
            })

            print("Result:", result)


if __name__ == "__main__":
    asyncio.run(main())



