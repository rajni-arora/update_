# server.py
from fastmcp import MCPServer, tool
from openai import OpenAI
import os

# Initialize OpenAI client (make sure OPENAI_API_KEY is in env)
client = OpenAI()

# Create an MCP server instance
app = MCPServer("gpt-tools-server")

@tool
def ask_gpt(question: str) -> str:
    """
    Ask GPT-4.1 a question and return the response.
    """
    response = client.chat.completions.create(
        model="gpt-4.1",   # Paid model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        max_tokens=200
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # Run MCP server
    app.run()
    
    
    
    
# client.py
from fastmcp.client import MCPClient

async def main():
    # Connect to MCP server
    async with MCPClient("gpt-tools-server", "stdio") as client:
        # Discover tools
        tools = await client.list_tools()
        print("Available tools:", [t.name for t in tools])

        # Call ask_gpt tool
        result = await client.call_tool("ask_gpt", {"question": "What is the capital of France?"})
        print("GPT says:", result.content[0].text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())