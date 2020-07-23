# Manufacturing Entropy - Code for the article
# Original Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# Data used in this file: pre-processed ("data/clean_manufacturing_paths.txt" and "data/clean_manufacturing_edges.txt")
# Yamila Mariel Omar
# Date of original code: 29th October 2019
# Date of code last modification: 21st July 2020



# ===== Function definitions ============

def add_self_loops(paths, edges):
    for k,v in paths.items():
        self_loop = (k[-1], k[-1])
        edges[self_loop] = edges.get(self_loop, 0) + v
    return edges




def generate_dot_file(graph, graph_name, filename):
    # File creation
    file_content = ''

    # General graph info
    file_content += 'digraph ' + graph_name + '{\n'
    file_content += 'size = "40,20";\n'
    file_content += 'graph[rankdir=TB, center=true, margin=0.05, nodesep=0.2, ranksep=0.5]\n'
    file_content += 'node[fontname="Courier-Bold", fontsize=14]\n'
    file_content += 'edge[arrowsize=0.2, arrowhead=normal]\n'

    for n in graph.nodes:
        file_content += str(n) + ' [shape=circle, style=filled, fontsize=20, color= orange, width=0.75, height=0.75, fixedsize=true]\n'

    for k,v in graph.edges.items():
        file_content += str(k[0]) + ' -> ' + str(k[1]) + ' [penwidth=1]\n'

    file_content += '}'

    path = "figures/" + filename
    with open(path, 'w') as f:
        f.write(file_content)
    return True

# ===== End Function definitions =========



if __name__ == "__main__":
    # Import needed modules
    # =====================
    from graphfile import GraphFile
    from graph import Graph
    import multiprocessing
    import datetime

    # Read data: clean paths and clean edges
    # ======================================
    filename_paths = "data/clean_manufacturing_paths.txt"
    filename_edges = "data/clean_manufacturing_edges.txt"
    edges = GraphFile(filename_edges).read_edges_from_file()
    paths = GraphFile(filename_paths).read_paths_with_count()

    # Generate graph from clean edges
    # ===============================
    edges = add_self_loops(paths, edges)
    G = Graph(edges)

    print("Number of nodes: ", len(G.nodes))
    print("Number of edges: ", len(G.edges.keys()))

    # Generate DOT file with network graph
    # ====================================
    generate_dot_file(G, "Bosch", "manufacturing_network_graph.dot")
