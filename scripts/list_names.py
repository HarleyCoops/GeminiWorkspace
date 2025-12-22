
import asyncio
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def list_names():
    with open("mcp_servers.json", "r") as f:
        config = json.load(f)
    jules_config = next(s for s in config["servers"] if s["name"] == "jules")
    server_params = StdioServerParameters(
        command=jules_config["command"],
        args=jules_config["args"],
        env={**os.environ, **jules_config["env"]}
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            for tool in tools.tools:
                print(tool.name)

if __name__ == "__main__":
    asyncio.run(list_names())
