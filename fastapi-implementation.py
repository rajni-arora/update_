from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver

# 1. Define state
class RewriteState(dict):
    # Input: query, config, knowledge_base_qr, etc.
    pass

# 2. Define the single QueryRewrite node
def query_rewrite_node(state):
    from services.query_rewrite.query_rewrite import QueryRewriteOrchestrator

    qr_service = QueryRewriteOrchestrator(state["config"])
    qr_response, qr_prompt = qr_service.query_rewrite_main(
        query=state["query"],
        knowledge_base_qr=state["knowledge_base_qr"],
        dynamic_examples=state["dynamic_examples"]
    )

    state.update({
        "rewritten_query": qr_response,
        "final_qr_prompt": qr_prompt
    })
    return state

# 3. Build graph with just one node
graph = StateGraph(RewriteState)

graph.add_node("QueryRewrite", query_rewrite_node)
graph.set_entry_point("QueryRewrite")
graph.add_edge("QueryRewrite", END)

# 4. Compile
query_rewrite_graph = graph.compile()

# 5. Example usage
if __name__ == "__main__":
    input_state = RewriteState({
        "query": "What is Gleam used for?",
        "knowledge_base_qr": ...,       # Replace with actual
        "dynamic_examples": ...,        # Replace with actual
        "config": ...                   # Replace with actual
    })

    final_state = query_rewrite_graph.invoke(input_state)
    print("Rewritten Query:", final_state["rewritten_query"])