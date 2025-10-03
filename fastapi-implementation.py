from safechain.tools.mcp import MCPToolAgent
import asyncio

async def main():
    # Connect to the MCP server over stdio
    async with MCPToolAgent("gpt-tools-server", transport="stdio") as client:
        # Discover tools
        tools = await client.list_tools()
        print("Available tools:", [t.name for t in tools])

        # Call the ask_gpt tool
        result = await client.call_tool("ask_gpt", {"question": "What is the capital of France?"})
        
        # Print GPT’s response
        print("GPT says:", result)

if __name__ == "__main__":
    asyncio.run(main())