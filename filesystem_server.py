from mcp import ServerSession, StdioServerParameters
import os

async def read_file(path: str) -> str:
    """Read the content of a file at the given path"""
    if not os.path.exists(path):
        return f"Error: File {path} not found"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

async def main():
    server = ServerSession(tools=[read_file])
    params = StdioServerParameters()
    await server.run(params)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())