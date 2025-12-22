
import asyncio
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def list_tools():
    # Load config from mcp_servers.json
    with open("mcp_servers.json", "r") as f:
        config = json.load(f)
    
    jules_config = next(s for s in config["servers"] if s["name"] == "jules")
    
    server_params = StdioServerParameters(
        command=jules_config["command"],
        args=jules_config["args"],
        env={**os.environ, **jules_config["env"]}
    )

    print(f"Connecting to {jules_config['name']}...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("\nAvailable Tools:")
            for tool in tools.tools:
                print(f"--- TOOL: {tool.name} ---")
                print(f"Description: {tool.description}")
                print(f"Schema: {json.dumps(tool.inputSchema, indent=2)}")
                print("-" * 20)

if __name__ == "__main__":
    asyncio.run(list_tools())
