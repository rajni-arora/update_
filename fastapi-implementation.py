# openai_client.py
import os
from openai import OpenAI

class OpenAIClient:
    """
    Handles all communication with OpenAI GPT models.
    """
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set it in .env or environment.")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def chat(self, messages, temperature=0.2, max_output_tokens=512):
        """
        Simulates a chat conversation using OpenAI GPT.
        `messages` is a list of dicts: [{"role": "system"/"user", "content": "..."}]
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_output_tokens,
        )
        return response.choices[0].message.content