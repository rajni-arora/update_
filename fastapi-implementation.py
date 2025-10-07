import os
import google.generativeai as genai

class GeminiClient:
    """
    Handles all communication with Google Gemini API.
    """

    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY environment variable.")
        genai.configure(api_key=self.api_key)
        self.model = model

    def chat(self, messages, temperature=0.2, max_output_tokens=512):
        """
        Simulates a chat conversation using the Gemini model.
        `messages` is a list of dicts: [{"role": "system"/"user", "content": "..."}]
        """
        # Combine all message content
        prompt_text = "\n".join([msg["content"] for msg in messages])
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(
            prompt_text,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens
            }
        )
        return response.text
        
        
        
        
        
# prompts.py
from typing import List, Dict

SUMMARY_PROMPT_SYSTEM = (
    "You are a helpful financial assistant. "
    "You analyze transaction summaries and provide concise, personalized financial insights, "
    "spending breakdowns, and saving suggestions."
)

def build_insight_prompt(transactions_summary: Dict, user_query: str) -> List[Dict]:
    """
    Build structured prompt messages for Gemini.
    """
    summary_text = "Transaction Summary:\n"
    for k, v in transactions_summary.items():
        summary_text += f"- {k}: {v}\n"

    user_message = f"""
User Query: {user_query}

{summary_text}

Please answer in this format:
1️⃣ Short Answer (1–2 lines)
2️⃣ 3 Actionable Insights
3️⃣ 2 Spending Trends
Make it concise, data-backed, and human-friendly.
"""
    return [
        {"role": "system", "content": SUMMARY_PROMPT_SYSTEM},
        {"role": "user", "content": user_message},
    ]
    
    
    
    
    
    
# processor.py
import pandas as pd
from typing import Dict, Any

def load_transactions_csv(path: str) -> pd.DataFrame:
    """Load transaction data from CSV."""
    df = pd.read_csv(path, parse_dates=["date"])
    return df

def summarize_transactions(df: pd.DataFrame, currency: str = "INR") -> Dict[str, Any]:
    """Compute spending summary and top categories."""
    df = df.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    now = pd.Timestamp.now()
    last_30 = df[df["date"] >= (now - pd.Timedelta(days=30))]

    summary = {
        "currency": currency,
        "total_spent_30d": f"{last_30['amount'].sum():.2f} {currency}",
        "total_spent_all": f"{df['amount'].sum():.2f} {currency}",
        "transaction_count_30d": int(last_30.shape[0]),
        "avg_daily_spend_30d": f"{(last_30['amount'].sum()/30):.2f} {currency}",
    }

    top_categories = last_30.groupby("category")["amount"].sum().sort_values(ascending=False).head(3)
    summary["top_categories_30d"] = {k: f"{v:.2f} {currency}" for k, v in top_categories.items()}
    return summary

def answer_user_query(gemini_client, df: pd.DataFrame, user_query: str) -> str:
    """Generate response using Gemini model."""
    from prompts import build_insight_prompt
    summary = summarize_transactions(df)
    messages = build_insight_prompt(summary, user_query)
    response = gemini_client.chat(messages)
    return response
    
    
    
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gemini_client import GeminiClient
from processor import load_transactions_csv, answer_user_query

app = FastAPI(title="GenAI Financial Assistant (Gemini)")

class QueryRequest(BaseModel):
    api_key: str | None = None
    query: str
    data_path: str = "sample_transactions.csv"

@app.post("/query")
def query_financial_assistant(req: QueryRequest):
    try:
        df = load_transactions_csv(req.data_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load data: {e}")

    try:
        gemini_client = GeminiClient(api_key=req.api_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        result = answer_user_query(gemini_client, df, req.query)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini processing failed: {e}")
        
        
        
        
import pandas as pd
from processor import summarize_transactions

def test_summary_basic():
    data = {
        "date": ["2025-09-01", "2025-09-02"],
        "description": ["Grocery", "Coffee"],
        "category": ["groceries", "food"],
        "amount": [100, 50],
        "currency": ["INR", "INR"]
    }
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    summary = summarize_transactions(df)
    assert "total_spent_all" in summary
    assert summary["currency"] == "INR"
    
    
    
fastapi==0.111.0
uvicorn==0.29.0
pandas==2.1.1
google-generativeai==0.7.2
pydantic==2.6.1
pytest==7.4.2
python-dotenv==1.0.0

date,description,category,amount,currency
2025-09-01,Grocery Store,groceries,45.20,INR
2025-09-02,Coffee Shop,food,3.50,INR
2025-09-05,Supermarket,groceries,120.75,INR
2025-09-10,Monthly Rent,rent,15000.00,INR
2025-09-12,Utility Bill,utilities,2200.00,INR
2025-09-13,Online Shopping,shopping,299.99,INR
2025-08-29,Train Ticket,transport,60.00,INR

pip install -r requirements.txt



Api key - AIzaSyAp9ulTLwe66fzFd7Yn_LAYW51fQz30uus



from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # load variables from .env file

class GeminiClient:
    def __init__(self, api_key=None, model="gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found. Please set it in .env or environment.")
        genai.configure(api_key=self.api_key)
        self.model = model






