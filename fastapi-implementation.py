import networkx as nx

class CreateGraph:
    def parse_triples(self, response_string):
        """
        Parse the final_output string into a list of (subject, predicate, object) triplets.
        """
        if not response_string:
            return []

        # Split by '\\n'
        raw_lines = response_string.strip().split("\\n")
        triplets = []

        for line in raw_lines:
            line = line.strip().strip("()`")  # remove surrounding quotes and parentheses
            if line:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) == 3:
                    triplets.append(parts)
        return triplets

    def create_graph_from_triplets(self, triplets):
        G = nx.DiGraph()
        for triplet in triplets:
            subject, predicate, obj = triplet
            G.add_edge(subject, obj, label=predicate)
        return G

    def select_subgraph(self, G, selected_nodes_list):
        selected_tree = []
        selected_preorder_nodes = []
        selected_postorder_nodes = []
        selected_labeled_edges = []

        for i in selected_nodes_list:
            selected_tree.append(list(nx.dfs_tree(G, source=i, depth_limit=3)))
            selected_preorder_nodes.append(list(nx.dfs_preorder_nodes(G, source=i, depth_limit=3)))
            selected_postorder_nodes.append(list(nx.dfs_postorder_nodes(G, source=i, depth_limit=3)))
            selected_labeled_edges.append(list(nx.dfs_labeled_edges(G, source=i, depth_limit=3)))

        return selected_tree, selected_preorder_nodes, selected_postorder_nodes, selected_labeled_edges