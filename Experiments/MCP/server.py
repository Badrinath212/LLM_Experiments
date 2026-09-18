from mcp.server import MCPServer

mcp = MCPServer("My Tools")

@mcp.tool()
def add_number(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def get_weather(city: str) -> str:
    return "It's raining in " + city

if __name__ == "__main__":
    mcp.run()
