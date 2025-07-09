from langgraph.graph import StateGraph, END

# Step 1: Define your node function
def query_rewrite_node(state):
    query = state["query"]
    print(f"📥 Input Query: {query}")

    # Example rewrite logic (replace with your actual logic)
    rewritten_query = query.replace("Get", "Retrieve")

    print(f"📤 Rewritten Query: {rewritten_query}")

    # Must return a dict with at least one key matching the state schema
    return {"rewritten_query": rewritten_query}

# Step 2: Define the state schema with output key(s)
builder = StateGraph(state_schema={
    "query": str,
    "rewritten_query": str
})

# Step 3: Add node, entry point, and edge to END
builder.add_node("QueryRewrite", query_rewrite_node)
builder.set_entry_point("QueryRewrite")
builder.add_edge("QueryRewrite", END)

# Step 4: Compile the graph
graph = builder.compile()

# Step 5: Run the graph with input
result = graph.invoke({
    "query": "Get amount of adults by product type and country"
})

# Step 6: Print final output state
print("✅ Final Updated State:", result)