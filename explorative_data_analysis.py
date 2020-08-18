# Manufacturing Entropy - Code for the article
# Original Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# Data used in this file: pre-processed ("data/clean_manufacturing_paths.txt" and "data/clean_manufacturing_edges.txt")
# Yamila Mariel Omar
# Date of original code: 6th August 2020
# Date of code last modification: 6th August 2020

# Explorative data analysis


# ===== Function definitions ============

def add_self_loops(paths, edges):
    for k,v in paths.items():
        self_loop = (k[-1], k[-1])
        edges[self_loop] = edges.get(self_loop, 0) + v
    return edges

# ===== END Function definitions ============



if __name__ == "__main__":
    # Import needed modules
    # =====================
    from graphfile import GraphFile
    from graph import Graph
    import datetime
    import matplotlib.pyplot as plt


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

    # ==========================================================================
    # Get frequency of n in paths
    # ==========================================================================
    freq_n_in_paths = {n:0 for n in G.nodes}
    for p,v in paths.items():
        for n in p:
            freq_n_in_paths[n] += v

    number_of_paths = sum(list(paths.values()))
    freq_n_in_paths = {k:v/number_of_paths for k,v in freq_n_in_paths.items()}

    # Make plot
    # =========
    x = list(freq_n_in_paths.keys())
    x.sort()
    freq = [freq_n_in_paths[n] for n in x]

    x_pos = [i for i, _ in enumerate(x)]

    plt.barh(x_pos, freq, color='red')
    plt.ylabel("Nodes")
    plt.xlabel("Frequency of n in manufacturing paths")

    plt.yticks(x_pos, x, fontsize=6)
    plt.savefig("figures/freq_n_in_paths.pdf")
    plt.close()


    # ==========================================================================
    # Get frequency of n as start node
    # ==========================================================================
    freq_start_nodes = dict()
    for p,v in paths.items():
        i = p[0]
        freq_start_nodes[i] = freq_start_nodes.get(i, 0) + v

    freq_start_nodes = {k:v/number_of_paths for k,v in freq_start_nodes.items()}

    # Make plot
    # =========
    x = list(freq_start_nodes.keys())
    x.sort()
    freq = [freq_start_nodes[n] for n in x]

    x_pos = [i for i, _ in enumerate(x)]

    plt.barh(x_pos, freq, color='red')
    plt.ylabel("Start Nodes")
    plt.xlabel("Freq. of n as start node in manufacturing paths")

    plt.yticks(x_pos, x, fontsize=6)
    plt.savefig("figures/freq_start_nodes.pdf")
    plt.close()

    # ==========================================================================
    # Get frequency of n as end node
    # ==========================================================================
    freq_end_nodes = dict()
    for p,v in paths.items():
        i = p[-1]
        freq_end_nodes[i] = freq_end_nodes.get(i, 0) + v

    freq_end_nodes = {k:v/number_of_paths for k,v in freq_end_nodes.items()}

    # Make plot
    # =========
    x = list(freq_end_nodes.keys())
    x.sort()
    freq = [freq_end_nodes[n] for n in x]

    x_pos = [i for i, _ in enumerate(x)]

    plt.barh(x_pos, freq, color='red')
    plt.ylabel("End Nodes")
    plt.xlabel("Freq. of n as end node in manufacturing paths")

    plt.yticks(x_pos, x, fontsize=6)
    plt.savefig("figures/freq_end_nodes.pdf")
    plt.close()

    # ==========================================================================
    # Strongly connected component
    # ==========================================================================
    edges = list(edges.keys())
    import networkx as nx
    G = nx.DiGraph()
    G.add_edges_from(edges)
    for scc in nx.strongly_connected_components(G):
        print(scc)
