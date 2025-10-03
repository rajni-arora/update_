from mcp.server.fastmcp import FastMCP
from safechain.lcel import model   # Import model like in test.py
from langchain_core.prompts import PromptTemplate

# Define host and port
host = "127.0.0.1"
port = 8000

# Initialize MCP server
mcp = FastMCP(
    name="mcp-pgvector-server",
    port=port,
    host=host,
)

# Define input prompt template
INPUT_PROMPT_TEMPLATE = """
You are an LLM engineer and knowledge graph expert. 
Please process the following text carefully and provide structured insights:

{text}
"""

# Register ask_gpt tool
@mcp.tool()
def ask_gpt(question: str) -> str:
    """
    Send the user question through a LangChain-style pipeline and return the response.
    """
    # Build LangChain prompt
    INPUT_PROMPT = PromptTemplate(
        input_variables=["text"],
        template=INPUT_PROMPT_TEMPLATE,
    )

    # Build pipeline (prompt -> model)
    chain = INPUT_PROMPT | model("3")

    # Invoke chain with user input
    result = chain.invoke({"text": question})
    llm_output = result.content

    return llm_output


if __name__ == "__main__":
    # Start MCP server
    mcp.run()