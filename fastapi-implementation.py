schema = {
    "employees": ["emp_id", "name", "department", "join_date", "salary"],
    "departments": ["dept_id", "dept_name", "manager_id"]
}


import networkx as nx
import matplotlib.pyplot as plt

def build_schema_graph(schema):
    G = nx.Graph()
    for table, columns in schema.items():
        G.add_node(table, type='table')
        for col in columns:
            G.add_node(col, type='column')
            G.add_edge(table, col)
    return G

def visualize_graph(G):
    pos = nx.spring_layout(G)
    node_colors = ['lightblue' if G.nodes[n]['type'] == 'table' else 'lightgreen' for n in G.nodes()]
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=10, font_weight='bold')
    plt.title("Knowledge Graph of Schema")
    plt.show()

# Usage
G = build_schema_graph(schema)
visualize_graph(G)



import re

def extract_keywords_from_query(query):
    # Very basic: extract words and lower case
    return re.findall(r'\w+', query.lower())

def find_relevant_schema(query, schema):
    keywords = extract_keywords_from_query(query)
    matched = {"tables": set(), "columns": set()}
    
    for table, columns in schema.items():
        if table in keywords:
            matched["tables"].add(table)
        for col in columns:
            if col in keywords:
                matched["columns"].add(col)
    return matched

# Example
query = "Show me employees who joined after 2020"
result = find_relevant_schema(query, schema)
print("Matched Tables:", result["tables"])
print("Matched Columns:", result["columns"])




def visualize_matched_graph(G, matched):
    pos = nx.spring_layout(G)
    node_colors = []
    for n in G.nodes():
        if n in matched['tables']:
            node_colors.append('red')
        elif n in matched['columns']:
            node_colors.append('orange')
        else:
            node_colors.append('lightgrey')
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=10)
    plt.title("Query-Matched Knowledge Graph")
    plt.show()

visualize_matched_graph(G, result)
