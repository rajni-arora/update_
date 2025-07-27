def get_tripalet(table_name_dict: dict, foreign_key_dict: dict, model_idx: str):
    from tqdm import tqdm
    import pandas as pd

    all_responses = []

    # Process one table at a time to reduce token usage
    for table_name, table_df in tqdm(table_name_dict.items()):

        # Process large tables in row batches
        batch_size = 50  # Adjust this to control token usage

        for i in range(0, len(table_df), batch_size):
            row_batch_df = table_df.iloc[i:i+batch_size]

            # redact
            try:
                redacted_schema = {table_name: perform_redact(row_batch_df.to_csv(index=False))}

                triple_extraction_prompt = Prompt  # Fix based on your setup
                input_node = {
                    "schema_dict": redacted_schema,
                    "foreign_key_dict": foreign_key_dict
                }

                response = model_invoke().model_call(
                    model_index=model_idx,
                    instruction_prompt=triple_extraction_prompt,
                    input_node=input_node
                )

                all_responses.append(response)

            except Exception as e:
                print(f"Error on table '{table_name}', rows {i}-{i+batch_size}: {e}")
    
    return all_responses