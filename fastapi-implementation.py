all_triples = []

for table_name, table_df in schema_table_dict.items():
    # Prepare just one table
    sub_table_dict = {table_name: table_df}

    # Filter relevant foreign keys only for that table (optional optimization)
    sub_fk_dict = {
        k: v for k, v in foreign_key_dict.items()
        if table_name in v or k.startswith(table_name)
    }

    try:
        print(f"Processing table: {table_name}")
        triples = get_tripalet(sub_table_dict, sub_fk_dict, model_idx="3")
        all_triples.append(triples)
    except Exception as e:
        print(f"Failed on {table_name} due to {e}")
        
        
final_output = "\n".join(str(t) for t in all_triples)