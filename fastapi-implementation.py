def get_triplet_batched(table_name_dict: Dict, foreign_key_dict: Dict, model_idx):
    all_triplets = []

    for table_name, table_df in table_name_dict.items():
        # Step 1: Prepare redacted schema for just one table
        table_csv = table_df.to_csv(index=False)
        redacted_schema = {table_name: perform_redact(table_csv)}

        # Step 2: Include only relevant FK keys (where this table is source or target)
        relevant_fks = {
            k: v for k, v in foreign_key_dict.items()
            if k == table_name or v["target_table"] == table_name
        }

        # Step 3: Prepare prompt and inputs
        triple_extraction_prompt = Prompt().triplate_extraction()
        input_node = {
            "schema_dict": redacted_schema,
            "foreign_key_dict": relevant_fks
        }

        # Step 4: Model Call
        response = model_invoke().model_call(
            model_index=model_idx,
            instruction_prompt=triple_extraction_prompt,
            input_node=input_node
        )

        # Step 5: Append output to combined result
        response_text = response.content if hasattr(response, 'content') else response
        all_triplets.append(response_text.strip())

    # Step 6: Merge all triplet texts into one final string
    final_output = "\n".join(all_triplets)
    return final_output