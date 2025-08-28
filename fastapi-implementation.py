import os
import yaml
import re
import logging
from dotenv import load_dotenv
from utils.llm import LLMService   # assumes you have this util class

# ----------------------
# Setup logging
# ----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------
# Load environment variables
# ----------------------
load_dotenv()   # this will read your .env file (API keys etc.)
# Example: os.getenv("OPENAI_API_KEY")

# ----------------------
# Load config from YAML
# ----------------------
def load_config(config_path: str):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# ----------------------
# Invoke LLM Chain
# ----------------------
def invoke_query_llm(config, rewrite_prompt: str):
    """
    Invokes LLM for query rewrite and returns raw response
    """
    llm_service = LLMService(config)
    response = llm_service.invoke_llm_chain(user_prompt=rewrite_prompt)
    return response

# ----------------------
# Generate Query Rewrite Response
# ----------------------
def generate_qr_response(config, qr_prompt: str):
    try:
        qr_response = invoke_query_llm(config, qr_prompt)
        logger.info("LLM call completed for query rewrite")

        # Extract "rewritten_query" from LLM response (assuming JSON-like output)
        final_qr_response = re.findall(r'"rewritten_query"\s*:\s*"([^"]+)"', qr_response)[0]

        return qr_response, final_qr_response
    except Exception as e:
        logger.error(f"Error from generate_qr_response: {e}")
        raise e

# ----------------------
# Main Execution
# ----------------------
if __name__ == "__main__":
    # Path to your config file
    config_path = "configs/ai_policy_config.yml"

    # Load config
    config = load_config(config_path)

    # Example input JSON with prompt
    qr_prompt = '{"prompt": "Convert code into key-value pairs"}'

    # Run
    qr_response, final_qr_response = generate_qr_response(config, qr_prompt)

    print("\n=== Raw LLM Response ===\n", qr_response)
    print("\n=== Final Extracted Response ===\n", final_qr_response)