from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Tools")

@mcp.tool()
def add_number(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def get_wheather(city: str) -> str:
    return "It's raining in " + city

if __name__ == "__main__":
    mcp.run()
