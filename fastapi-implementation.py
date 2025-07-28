def get_tripalet(table_name_dict: Dict, foreign_key_dict: Dict, model_idx: str):
    all_responses = {}  # To store responses per table

    for table_name, table_df in table_name_dict.items():
        # Redact the schema for this single table
        redact_schema = {
            table_name: perform_redact(table_df.to_csv(index=False))
        }

        # Prepare prompt
        triple_extraction_prompt = Prompt().triplet_extraction()
        input_node = {
            "schema_dict": redact_schema,
            "foreign_key_dict": foreign_key_dict
        }

        try:
            # Call the model
            response = model_invoke().model_call(
                model_index=model_idx,
                instruction_prompt=triple_extraction_prompt,
                input_node=input_node
            )
            all_responses[table_name] = response

        except Exception as e:
            print(f"Failed to process {table_name}: {e}")
            all_responses[table_name] = None

    return all_responses