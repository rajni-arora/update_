from mcp.server.fastmcp import FastMCP
from safechain.tools.mcp import MCPToolLoader
from safechain.lcel import model   # Import model like in test.py
from langchain_core.prompts import PromptTemplate

# Use MCPToolLoader
tool_loader = MCPToolLoader()

# Define input prompt template (like in test.py)
INPUT_PROMPT_TEMPLATE = """
You are an LLM engineer and knowledge graph expert. 
Please process the following text carefully and provide structured insights:

{text}
"""

@tool_loader.tool
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

    # Invoke the chain with user input
    result = chain.invoke({"text": question})
    llm_output = result.content

    return llm_output


if __name__ == "__main__":
    # Create and run MCP server instance, registering the ask_gpt tool
    app = FastMCP("gpt-tools-server", tools=tool_loader.tools)
    app.run()