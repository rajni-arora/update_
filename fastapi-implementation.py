from mcp.server.fastmcp import FastMCP
from safechain.tools.mcp import MCPToolLoader, MCPToolAgent
from openai import OpenAI  # Make sure openai is installed

# Initialize OpenAI client (make sure OPENAI_API_KEY is in env)
client = OpenAI()

# Use MCPToolLoader instead of missing "tool"
tool_loader = MCPToolLoader()

@tool_loader.tool
def ask_gpt(question: str) -> str:
    """
    Ask GPT-4.1 a question and return the response.
    """
    response = client.chat.completions.create(
        model="gpt-4.1",  # Paid model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        max_tokens=200
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # Create and run MCP server instance, registering the ask_gpt tool
    app = FastMCP("gpt-tools-server", tools=tool_loader.tools)
    app.run()