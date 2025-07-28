triples_obj = CreateGraph()
triplets_dict = {}

for table, ai_msg in triples.items():
    if ai_msg is not None:
        try:
            triplets_dict[table] = triples_obj.parse_triples(ai_msg)
        except Exception as e:
            print(f"Error parsing triples for {table}: {e}")
            triplets_dict[table] = []