from mcp.server.fastmcp import FastMCP
from safechain.tools.mcp import MCPToolLoader
from openai import OpenAI  # Make sure openai is installed
from langchain_core.prompts import PromptTemplate
import os

# Initialize OpenAI client (make sure OPENAI_API_KEY is in env)
client = OpenAI()

# Use MCPToolLoader
tool_loader = MCPToolLoader()

# Define input prompt template (like in test.py)
INPUT_PROMPT_TEMPLATE = """
You are an LLM engineer and knowledge graph expert. 
Please process the following text carefully and provide structured insights:

{text}
"""

# Register ask_gpt tool
@tool_loader.tool
def ask_gpt(question: str) -> str:
    """
    Send the user question to GPT and return the response.
    """
    # Build prompt
    prompt = PromptTemplate(
        input_variables=["text"],
        template=INPUT_PROMPT_TEMPLATE,
    )
    formatted_prompt = prompt.format(text=question)

    # Call GPT
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": formatted_prompt},
        ],
        max_tokens=200,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # Create and run MCP server instance, registering the ask_gpt tool
    app = FastMCP("gpt-tools-server", tools=tool_loader.tools)
    app.run()
    
    

from safechain.tools.mcp import MCPToolAgent
import asyncio

async def main():
    # Take input from user
    user_input = input("Enter your question: ")

    # Connect to the MCP server over stdio
    async with MCPToolAgent("gpt-tools-server", transport="stdio") as client:
        # Discover available tools
        tools = await client.list_tools()
        print("Available tools:", [t.name for t in tools])

        # Call the ask_gpt tool with user input
        result = await client.call_tool("ask_gpt", {"question": user_input})

        # Print GPT's response
        print("GPT says:", result)

if __name__ == "__main__":
    asyncio.run(main())
