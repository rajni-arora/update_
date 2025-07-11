from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

# --- 1. Define State ---
class QueryServingState(TypedDict, total=False):
    input_query: str
    gated: bool
    rewritten_query: Optional[str]
    sl_retrieval_output: Optional[dict]
    sl_output: Optional[dict]
    sql_output: Optional[str]
    sql_validated: bool

# --- 2. Dummy Node Functions (wire your services here) ---
def node_gating(state: QueryServingState) -> QueryServingState:
    print("Running Gating...")
    state["gated"] = True  # or some gating logic
    return state

def node_retrieval_datastax(state: QueryServingState) -> QueryServingState:
    print("Retrieving from Datastax...")
    return state

def node_retrieval_tfidf(state: QueryServingState) -> QueryServingState:
    print("TF-IDF Retrieval...")
    return state

def node_query_rewrite(state: QueryServingState) -> QueryServingState:
    print("Query Rewrite in Progress...")
    state["rewritten_query"] = f"Rewritten({state['input_query']})"
    return state

def node_sl_retrieval(state: QueryServingState) -> QueryServingState:
    print("SL Retrieval...")
    state["sl_retrieval_output"] = {"top_k": ["result1", "result2"]}
    return state

def node_sl_reranking(state: QueryServingState) -> QueryServingState:
    print("SL Reranking...")
    return state

def node_sl(state: QueryServingState) -> QueryServingState:
    print("SL Processing...")
    state["sl_output"] = {"result": "linked schema"}
    return state

def node_few_shot(state: QueryServingState) -> QueryServingState:
    print("Few-Shot Query Serving...")
    return state

def node_query_process(state: QueryServingState) -> QueryServingState:
    print("Serving Process Channel...")
    return state

def node_sql_validator(state: QueryServingState) -> QueryServingState:
    print("SQL Validator running...")
    state["sql_validated"] = True
    return state

def node_sql_ranking(state: QueryServingState) -> QueryServingState:
    print("SQL Ranking...")
    return state

def node_sql_output(state: QueryServingState) -> QueryServingState:
    print("Generating SQL Output...")
    state["sql_output"] = "SELECT * FROM table WHERE condition"
    return state

# --- 3. Create LangGraph ---
builder = StateGraph(QueryServingState)

# --- 4. Add Nodes ---
builder.add_node("Gating", node_gating)
builder.add_node("Retrieval_Datastax", node_retrieval_datastax)
builder.add_node("Retrieval_TFIDF", node_retrieval_tfidf)
builder.add_node("Query_Rewrite", node_query_rewrite)
builder.add_node("SL_Retrieval", node_sl_retrieval)
builder.add_node("SL_Reranking", node_sl_reranking)
builder.add_node("SL", node_sl)
builder.add_node("Few_Shot", node_few_shot)
builder.add_node("Query_Process", node_query_process)
builder.add_node("SQL_Validator", node_sql_validator)
builder.add_node("SQL_Ranking", node_sql_ranking)
builder.add_node("SQL_Output", node_sql_output)

# --- 5. Define Edges (based on diagram flow) ---
builder.set_entry_point("Gating")
builder.add_edge("Gating", "Retrieval_Datastax")
builder.add_edge("Retrieval_Datastax", "Retrieval_TFIDF")
builder.add_edge("Retrieval_TFIDF", "Query_Rewrite")
builder.add_edge("Query_Rewrite", "SL_Retrieval")
builder.add_edge("SL_Retrieval", "SL_Reranking")
builder.add_edge("SL_Reranking", "SL")
builder.add_edge("SL", "Few_Shot")
builder.add_edge("Few_Shot", "Query_Process")
builder.add_edge("Query_Process", "SQL_Validator")
builder.add_edge("SQL_Validator", "SQL_Ranking")
builder.add_edge("SQL_Ranking", "SQL_Output")
builder.add_edge("SQL_Output", END)

# --- 6. Compile the graph ---
app = builder.compile()

# --- 7. Run with Dummy Input ---
inputs = {
    "input_query": "Show me all transactions for last month"
}

print("\n--- LangGraph Output ---\n")
final_state = app.invoke(inputs)
print(final_state)