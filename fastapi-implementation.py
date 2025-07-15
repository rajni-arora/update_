def qr_human_validation_node(state: QueryServingState) -> QueryServingState:
    print("Rewritten Query:", state["rewritten_query"])
    user_input = input("Do you want to proceed with the rewritten query? (yes/no): ").strip().lower()

    if user_input != "yes":
        raise Exception("Human validation failed. Stopping the pipeline.")
    
    return state
    
    
    
g.add_node("qr_human_validation", qr_human_validation_node)
g.add_edge("qr_query_rewrite", "sl_datastax")



g.add_edge("qr_query_rewrite", "qr_human_validation")
g.add_edge("qr_human_validation", "sl_datastax")


def build_query_serving_graph(config):
    g = StateGraph(QueryServingState)

    g.add_node("qr_gating", lambda state: qr_gating_node(state, config))
    g.add_node("qr_datastax", qr_datastax_node)
    g.add_node("qr_knowledge", qr_knowledge_node)
    g.add_node("qr_query_rewrite", qr_query_rewrite_node)
    g.add_node("qr_human_validation", qr_human_validation_node)  # 👈 NEW

    g.add_node("sl_datastax", sl_datastax_node)
    g.add_node("sl_rerank_schema", sl_rerank_schema_node)
    g.add_node("sg_fewshot", sg_fewshot_node)
    g.add_node("sg_schema_prompt", sg_schema_prompt_node)
    g.add_node("sg_process_channel", sg_process_channel_node)
    g.add_node("sg_sql_ranking", sg_sql_ranking_node)

    g.add_edge("qr_gating", "qr_datastax")
    g.add_edge("qr_datastax", "qr_knowledge")
    g.add_edge("qr_knowledge", "qr_query_rewrite")
    g.add_edge("qr_query_rewrite", "qr_human_validation")  # 👈 NEW
    g.add_edge("qr_human_validation", "sl_datastax")       # 👈 NEW
    g.add_edge("sl_datastax", "sl_rerank_schema")
    g.add_edge("sl_rerank_schema", "sg_fewshot")
    g.add_edge("sg_fewshot", "sg_schema_prompt")
    g.add_edge("sg_schema_prompt", "sg_process_channel")
    g.add_edge("sg_process_channel", "sg_sql_ranking")

    g.set_entry_point("qr_gating")
    return g.compile()
