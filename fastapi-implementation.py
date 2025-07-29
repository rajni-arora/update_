from typing import Dict

def get_tripalet_loopwise(table_name_dict: Dict, foreign_key_dict, model_idx):
    final_response = []

    # Convert foreign key dict to DataFrame if not already
    if not isinstance(foreign_key_dict, pd.DataFrame):
        print("foreign_key_dict should be a pandas DataFrame with columns: table1, column1, table2, column2")
        return

    # Iterate row-by-row through foreign key mappings
    for idx, row in foreign_key_dict.iterrows():
        table1 = row['table1']
        table2 = row['table2']

        if table1 not in table_name_dict or table2 not in table_name_dict:
            continue  # Skip if any table not present

        # Redact schema for both involved tables
        redact_schema = {
            table1: perform_redact(table_name_dict[table1].to_csv(index=False)),
            table2: perform_redact(table_name_dict[table2].to_csv(index=False))
        }

        # Prepare prompt and input
        triple_extraction_prompt = Prompt().triplate_extraction()
        input_node = {
            "schema_dict": redact_schema,
            "foreign_key_dict": pd.DataFrame([row]).to_dict(orient="records")[0]  # send only current row
        }

        # Call model
        response = model_invoke().model_call(
            model_index=model_idx,
            instruction_prompt=triple_extraction_prompt,
            input_node=input_node
        )

        final_response.append(response)

    return final_response