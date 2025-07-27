def get_tripalet(table_name_dict: dict, foreign_key_dict: dict, model_idx: str):
    from tqdm import tqdm  # optional: for progress bar
    all_responses = []
    
    # Convert to list for slicing
    data_items = list(table_name_dict.items())
    
    batch_size = 50  # You can tune this (10, 20, 100) depending on token usage
    
    for i in tqdm(range(0, len(data_items), batch_size)):
        batch = dict(data_items[i:i+batch_size])
        
        # redact the schema
        redact_schema = {
            table_name: perform_redact(table_df.to_csv(index=False))
            for table_name, table_df in batch.items()
        }

        triple_extraction_prompt = Prompt().triplet_extraction_prompt()
        
        input_node = {
            "schema_dict": redact_schema,
            "foreign_key_dict": foreign_key_dict
        }

        try:
            response = model_invoke().model_call(
                model_index=model_idx,
                instruction_prompt=triple_extraction_prompt,
                input_node=input_node
            )
            all_responses.append(response)
        except Exception as e:
            print(f"Error processing batch {i}-{i+batch_size}: {e}")
    
    return all_responses