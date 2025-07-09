from langgraph.graph import StateGraph, END

# 1. Define the state schema explicitly
class RewriteState(dict):
    # This dict will carry all data through the node
    pass

# 2. Node definition
def query_rewrite_node(state):
    from services.query_rewrite.query_rewrite import QueryRewriteOrchestrator

    print("📥 Input Query:", state.get("query"))

    qr_service = QueryRewriteOrchestrator(state["config"])
    qr_response, qr_prompt = qr_service.query_rewrite_main(
        query=state["query"],
        knowledge_base_qr=state["knowledge_base_qr"],
        dynamic_examples=state["dynamic_examples"]
    )

    print("📤 Rewritten Query:", qr_response)
    print("🧠 Prompt Used:", qr_prompt)

    # Return updated state (must include at least one key!)
    return {
        "rewritten_query": qr_response,
        "final_qr_prompt": qr_prompt
    }

# 3. Build the graph
# Define which keys are tracked in the state
builder = StateGraph(state_schema={
    "query": str,
    "knowledge_base_qr": object,  # replace `object` with actual type if known
    "dynamic_examples": object,   # same here
    "config": object,
    "rewritten_query": str,
    "final_qr_prompt": str
})

# 4. Add node and edges
builder.add_node("QueryRewrite", query_rewrite_node)
builder.set_entry_point("QueryRewrite")
builder.add_edge("QueryRewrite", END)

# 5. Compile the graph
query_rewrite_graph = builder.compile()

# 6. Run with example input
if __name__ == "__main__":
    input_state = {
        "query": "What is Gleam used for?",
        "knowledge_base_qr": ...,       # Replace with actual KB object
        "dynamic_examples": ...,        # Replace with actual examples
        "config": ...                   # Replace with your config
    }

    result = query_rewrite_graph.invoke(input_state)

    print("\n✅ Final Updated State:")
    for k, v in result.items():
        print(f"{k}: {v}")