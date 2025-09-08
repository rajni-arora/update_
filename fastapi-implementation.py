import requests

def qr_human_validation_node(state: QueryServingState) -> QueryServingState:
    print("Query Rewrite Human Validation Node")

    # API endpoint
    url = "https://gleamusersessionmgmt-qa.aexp.com/langgraphPayloadRetrieval"
    
    # Request body (dynamic chat_id can come from state if available)
    payload = {
        "chat_id": state.get("chat_id", "9ba87391-8ff5-4f04-9981-e8e113816193"),
        "role": "SL"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Extract query from API response
        api_query = data["msg_da"]["query"]

        # Use this query as the validated query
        state["user_response_gr"] = "yes"   # Assume API auto-approves
        state["rewritten_query"] = api_query  

        print(f"API returned query: {api_query}")

    except Exception as e:
        print(f"Error calling API: {e}")
        # fallback to original query if API fails
        state["user_response_gr"] = "no"
        state["rewritten_query"] = state["query"]

    return state