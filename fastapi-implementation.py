from mcp.server.fastmcp import FastMCP
from safechain.tools.mcp import MCPToolLoader
from openai import OpenAI  # Make sure openai is installed
import os

# Initialize OpenAI client (make sure OPENAI_API_KEY is in env)
client = OpenAI()

# Use MCPToolLoader to register tools
tool_loader = MCPToolLoader()

# Define a prompt template (similar to your test.py)
INPUT_PROMPT_TEMPLATE = """
Imagine you are an LLM engineer and a knowledge graph expert.
For the following content, extract the following:
Community

Content:
{text}
"""

@tool_loader.tool
def extract_community(text: str) -> str:
    """
    Extract community-related entities from the given text using GPT-4.1.
    """
    response = client.chat.completions.create(
        model="gpt-4.1",  # Paid model
        messages=[
            {"role": "system", "content": "You are an expert entity extractor."},
            {"role": "user", "content": INPUT_PROMPT_TEMPLATE.format(text=text)},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()

@tool_loader.tool
def ask_gpt(question: str) -> str:
    """
    General Q&A with GPT-4.1.
    """
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # Create and run MCP server instance, registering tools
    app = FastMCP("gpt-tools-server", tools=tool_loader.tools)
    app.run()