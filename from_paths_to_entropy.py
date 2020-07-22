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



def calculate_entropy(G, p_ij):
    ''' '''
    from math import log

    C_H = {i:0 for i in G.nodes}
    for i in G.nodes:
        for j in G.nodes:
            if p_ij[(i,j)] != 0:
                C_H[i] = C_H[i] + p_ij[(i,j)] * log(p_ij[(i,j)], 2)
    C_H = {k:-v for k,v in C_H.items()}
    return C_H

# ===== End Function definitions =========



if __name__ == "__main__":
    # Import needed modules
    # =====================
    from graphfile import GraphFile
    from graph import Graph
    import multiprocessing
    import datetime
    import sys

    method = int(sys.argv[1])

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
    if method == 1:
        # # Method 1: finding all paths in the graph
        # # Due to computation issues, this is deployed in an HPC!!!
        # # ========================================================
        # pool = multiprocessing.Pool()
        # start = datetime.datetime.now()
        # print("Start time: ", start)
        # r = pool.map(G.get_node_entropy, G.nodes)
        # end = datetime.datetime.now()
        # print("End time: ", end)
        # print("Run time: ", end - start)
        # pool.close()
        # pool.join()
        #
        # C_H_method1 = {i:C for (i,C) in r}
        #
        # GraphFile("results/entropy_method_1.txt").write_centrality_values_to_file(C_H_method1)
        print("Method 1 must be run in the HPC!")


    elif method == 2:
        # Method 2: using manufacturing paths
        # ===================================
        p_ij = {(i,j):0 for i in G.nodes for j in G.nodes}
        for path in paths:
            i, j, p = G._path_probability(path)
            p_ij[(i,j)] += p

        C_H_method2 = calculate_entropy(G, p_ij)
        GraphFile("results/entropy_method_2.txt").write_centrality_values_to_file(C_H_method2)

    elif method == 3:
        # Method 3: using manufacturing paths (accounting for subpaths)
        # =============================================================
        p_ij = {(i,j):0 for i in G.nodes for j in G.nodes}
        seen_paths = set()

        for path in paths:
            for index in range(len(path)):
                p = tuple(path[index: ])
                if p not in seen_paths:
                    i, j, prob = G._path_probability(p)
                    p_ij[(i,j)] += prob
                    seen_paths.add(p)

        C_H_method3 = calculate_entropy(G, p_ij)
        GraphFile("results/entropy_method_3.txt").write_centrality_values_to_file(C_H_method3)



    elif method == 4:
        # Method 4: ignoring paths, i.e. source-sink probability
        # ======================================================
        number_of_manufactured_items = sum(list(paths.values()))

        p_ij = {(i,j):0 for i in G.nodes for j in G.nodes}
        for path, freq in paths.items():
            i, j = path[0], path[-1]
            p_ij[(i,j)] += freq / number_of_manufactured_items

        C_H_method4 = calculate_entropy(G, p_ij)
        GraphFile("results/entropy_method_4.txt").write_centrality_values_to_file(C_H_method4)



    else:
        print("Method {} does not exist!".format(method))
