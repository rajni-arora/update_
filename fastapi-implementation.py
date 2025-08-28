import os
import yaml
import re
import json
import logging
from dotenv import load_dotenv
from utils.llm import LLMService   # you already have this util

# ----------------------
# Setup logging
# ----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------
# Load environment variables
# ----------------------
load_dotenv()   # reads .env file
# Example: OPENAI_API_KEY is now available via os.getenv("OPENAI_API_KEY")

# ----------------------
# Load config from YAML
# ----------------------
def load_config(config_path: str):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# ----------------------
# Invoke LLM Chain
# ----------------------
def invoke_query_llm(config, input_json: dict):
    """
    Invokes LLM for query rewrite and returns raw response
    """
    llm_service = LLMService(config)

    # Extract the prompt from JSON
    rewrite_prompt = input_json.get("prompt", "")

    response = llm_service.invoke_llm_chain(user_prompt=rewrite_prompt)
    return response

# ----------------------
# Generate Query Rewrite Response
# ----------------------
def generate_qr_response(config, input_json: dict):
    try:
        qr_response = invoke_query_llm(config, input_json)
        logger.info("LLM call completed for query rewrite")

        # Try to extract rewritten_query if returned in JSON-like format
        final_qr_response = None
        try:
            final_qr_response = re.findall(r'"rewritten_query"\s*:\s*"([^"]+)"', qr_response)[0]
        except Exception:
            logger.warning("Could not extract `rewritten_query` field. Returning raw response.")

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

    # Example JSON input (your extracted PDF content will go in "content")
    input_json = {
        "prompt": "Convert the following PDF text into key-value pairs",
        "content": "Invoice Number: 12345 Date: 2025-08-28 Customer: John Doe"
    }

    # Run
    qr_response, final_qr_response = generate_qr_response(config, input_json)

    print("\n=== Raw LLM Response ===\n", qr_response)
    print("\n=== Final Extracted Response (if found) ===\n", final_qr_response)