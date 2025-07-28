triples_obj = CreateGraph()
triplets_dict = {}

for table, ai_msg in triples.items():
    if ai_msg is not None:
        try:
            triplets_dict[table] = triples_obj.parse_triples(ai_msg)
        except Exception as e:
            print(f"Error parsing triples for {table}: {e}")
            triplets_dict[table] = [
            
            
            
            
import networkx as nx
import matplotlib.pyplot as plt

class CreateGraph:
    def parse_triples(self, response, delimiter="\n"):
        if not response:
            return []
        if hasattr(response, 'content'):
            return response.content.split(delimiter)
        if isinstance(response, str):
            return response.split(delimiter)
        raise ValueError("Unsupported response format")

    def create_graph_from_triplets(self, triplets):
        G = nx.DiGraph()
        substring = "→"  # adjust if you're using another delimiter/symbol
        for triplet in triplets:
            count = triplet.count(substring)
            if count == 2:
                subject, predicate, obj = triplet.strip().split(substring)
                G.add_edge(subject.strip(), obj.strip(), label=predicate.strip())
            elif count > 2:
                string_tuple = triplet.strip().split(substring)
                subject = string_tuple[0]
                predicate = string_tuple[1]
                obj = "→".join(string_tuple[2:])
                G.add_edge(subject.strip(), obj.strip(), label=predicate.strip())
        return G

def visualize_kg(G: nx.DiGraph, table_name: str):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=8, arrows=True)

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

    plt.title(f"Knowledge Graph - {table_name}")
    plt.savefig(f'KG_{table_name}.png')
    plt.close()

# ----- RUN ALL -----
# Input: triples (your dict with AIMessage per table)
triples_obj = CreateGraph()
triplets_dict = {}

# Parse triplets from AI messages
for table, ai_msg in triples.items():
    if ai_msg is not None:
        triplets_dict[table] = triples_obj.parse_triples(ai_msg)

# Create and visualize each graph
for table, triplet_list in triplets_dict.items():
    G = triples_obj.create_graph_from_triplets(triplet_list)
    visualize_kg(G, table)

print("✅ All graphs generated and saved.")