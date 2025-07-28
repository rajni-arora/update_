def create_graph_from_triplets(self, triplets):
    G = nx.DiGraph()
    
    for triplet in triplets:
        # Choose delimiter based on what's in the string
        if "→" in triplet:
            parts = triplet.strip().split("→")
        elif "->" in triplet:
            parts = triplet.strip().split("->")
        elif "," in triplet:
            parts = triplet.strip().split(",")
        else:
            continue  # skip malformed triplet

        parts = [p.strip() for p in parts]
        
        if len(parts) >= 3:
            subject = parts[0]
            predicate = parts[1]
            obj = " ".join(parts[2:])
            G.add_edge(subject, obj, label=predicate)

    return G