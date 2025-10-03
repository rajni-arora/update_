from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from openai import OpenAI

# Initialize OpenAI client (make sure OPENAI_API_KEY is set in your env)
client = OpenAI()

app = FastAPI()

# Request body schema
class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_gpt(query: Query):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",  # Paid GPT model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query.question}
            ],
            max_tokens=200
        )
        answer = response.choices[0].message.content
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
    
    
    
    
    
import requests

SERVER_URL = "http://127.0.0.1:8000/ask"

def start_client():
    print("Connected to AI server. Type 'exit' to quit.\n")
    while True:
        question = input("You: ")
        if question.lower() == "exit":
            break
        
        response = requests.post(SERVER_URL, json={"question": question})
        if response.status_code == 200:
            print("GPT:", response.json().get("answer"))
        else:
            print("Error:", response.text)

if __name__ == "__main__":
    start_client()