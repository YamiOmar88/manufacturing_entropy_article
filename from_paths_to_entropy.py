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

    # =========================================================================
    # CALCULATE ENTROPY
    # =========================================================================

    # Method 1: finding all paths in the graph
    # ========================================
    pool = multiprocessing.Pool()
    start = datetime.datetime.now()
    print("Start time: ", start)
    r = pool.map(G.get_node_entropy, G.nodes)
    end = datetime.datetime.now()
    print("End time: ", end)
    print("Run time: ", end - start)
    pool.close()
    pool.join()

    C_H = {i:C for (i,C) in r}

    GraphFile("results/entropy_method_1.txt").write_centrality_values_to_file(C_H)
