from mcp.server import MCPServer
from typing import Literal

mcp = MCPServer("My Tools")

@mcp.tool()
def add_number(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def get_weather(city: str, 
                unit: Literal["celsius", "fahrenheit"] = "celsius") -> str:
    """Get the weather for a city."""
    return "It's raining in " + city

if __name__ == "__main__":
    mcp.run()
