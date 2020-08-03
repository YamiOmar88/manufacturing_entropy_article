# Manufacturing Entropy - Code for the article
# Original Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# Data used in this file: pre-processed ("data/clean_manufacturing_paths.txt" and "data/clean_manufacturing_edges.txt")
# Yamila Mariel Omar
# Date of original code: 29th October 2019
# Date of code last modification: 3rd August 2020



# ===== Function definitions ============

def add_self_loops(paths, edges):
    for k,v in paths.items():
        self_loop = (k[-1], k[-1])
        edges[self_loop] = edges.get(self_loop, 0) + v
    return edges



def calculate_entropy(G, p_ij):
    '''Auxiliary function to calculate the entropy centrality without using the
    class method in graph.py.
    Input variables:
    - G: graph (see graph.py for details)
    - p_ij: dictionary of path probabilities. Keys are (i,j) node pairs, and
    values are probabilities.
    Output variables:
    - C_H: dictionary of entropy centrality. Keys are nodes and values are their
    entropy centrality.
    '''
    from math import log

    C_H = {i:0 for i in G.nodes}
    for i in G.nodes:
        for j in G.nodes:
            if p_ij[(i,j)] != 0:
                C_H[i] = C_H[i] + p_ij[(i,j)] * log(p_ij[(i,j)], 2)
    C_H = {k:-v for k,v in C_H.items()}
    return C_H



def find_all_subpaths_of_path(path):
    '''
    This function finds all subpaths of a path.
    Input variables:
    - path: tuple containing a path.
    Output variables:
    - subpaths: set of subpaths in path.

    Example:
    path = (1, 2, 3, 4)
    >>> find_all_subpaths_of_path(path)
    {(1, 2), (1, 2, 3, 4), (1,), (2,), (3,), (1, 2, 3), (4,), (2, 3), (2, 3, 4), (3, 4)}
    '''
    subpaths = set()
    for i in range(len(path)):
        for j in range(i+1, len(path)+1):
            subpaths.add( path[i:j] )
    return subpaths


def normalize_p_ij(p_ij, nodes):
    '''Shannon's entropy is defined for sum(p_i) = 1. This function normalizes
    p_ij so the Shannon's entropy can be calculated.
    Input variables:
    - p_ij: dictionary of probabilities
    - nodes: set of graph nodes
    Outupt varaibles:
    - p_ij_normalized: normalized probabilities
    '''
    p_i = {n:0 for n in nodes}
    for i in nodes:
        for j in nodes:
            p_i[i] += p_ij[(i,j)]

    p_ij_normalized = dict()
    for k,v in p_ij.items():
        i = k[0]
        if p_i[i] != 0:
            p_ij_normalized[k] = v / p_i[i]
        else:
            p_ij_normalized[k] = v

    return p_ij_normalized


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
    # full_path = "/mnt/irisgpfs/users/yomar/manufacturing_entropy_article/"
    filename_paths = "data/clean_manufacturing_paths.txt"
    # filename_paths = full_path + filename_paths
    filename_edges = "data/clean_manufacturing_edges.txt"
    # filename_edges = full_path + filename_edges
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
        # Method 1: finding all paths in the graph
        # Due to computation issues, this is deployed in an HPC!!!
        # ========================================================
        print("Method 1: Tutzauer's formulation (all paths in graph)")
        pool = multiprocessing.Pool()
        start = datetime.datetime.now()
        input_variables = zip(G.nodes, ["Other"]*len(G.nodes))
        print("Start time: ", start)
        r = pool.starmap(G.calculate_node_entropy, input_variables)
        end = datetime.datetime.now()
        print("End time: ", end)
        print("Run time: ", end - start)
        pool.close()
        pool.join()

        C_H = {i:C for (i,C) in r}

        end_date = end.strftime("%Y_%m_%d_")
        filename = "results/" + end_date + "entropy_method_1.txt"
        GraphFile(full_path + filename).write_centrality_values_to_file(C_H)



    elif method == 2:
        # Method 2: using manufacturing paths
        # ===================================
        print("Method 2: Tutzauer's formulation using manufacturing paths")
        p_ij = {(i,j):0 for i in G.nodes for j in G.nodes}
        for path in paths:
            i, j, p = G._path_probability(path, formulation_type="Tutzauer")
            p_ij[(i,j)] += p

        p_ij_n = normalize_p_ij(p_ij, G.nodes)

        C_H = calculate_entropy(G, p_ij_n)

        end_date = datetime.datetime.now().strftime("%Y_%m_%d_")
        filename = "results/" + end_date + "entropy_method_2.txt"
        GraphFile(filename).write_centrality_values_to_file(C_H)


    elif method == 3:
        # Method 3: newly defined path probability (all paths in graph)
        # Due to computation issues, this is deployed in an HPC!!!
        # =============================================================
        print("Method 3: newly defined path probability (all paths in graph)")
        pool = multiprocessing.Pool()
        start = datetime.datetime.now()
        input_variables = zip(G.nodes, ["Other"]*len(G.nodes))
        print("Start time: ", start)
        r = pool.starmap(G.calculate_node_entropy, input_variables)
        end = datetime.datetime.now()
        print("End time: ", end)
        print("Run time: ", end - start)
        pool.close()
        pool.join()

        C_H = {i:C for (i,C) in r}

        end_date = end.strftime("%Y_%m_%d_")
        filename = "results/" + end_date + "entropy_method_3.txt"
        GraphFile(full_path + filename).write_centrality_values_to_file(C_H)


    elif method == 4:
        # Method 4: newly defined path probability (manufacturing paths)
        # =============================================================
        print("Method 4: Alternative formulation using manufacturing paths")
        p_ij = {(i,j):0 for i in G.nodes for j in G.nodes}
        for path in paths:
            i, j, p = G._path_probability(path, formulation_type="Other")
            p_ij[(i,j)] += p

        p_ij_n = normalize_p_ij(p_ij, G.nodes)

        C_H = calculate_entropy(G, p_ij_n)

        end_date = datetime.datetime.now().strftime("%Y_%m_%d_")
        filename = "results/" + end_date + "entropy_method_4.txt"
        GraphFile(filename).write_centrality_values_to_file(C_H)



    elif method == 5:
        # Method 5: ignoring paths, i.e. source-sink probability
        # ======================================================
        number_of_manufactured_items = sum(list(paths.values()))

        p_ij = {(i,j):0 for i in G.nodes for j in G.nodes}
        for path, freq in paths.items():
            i, j = path[0], path[-1]
            p_ij[(i,j)] += freq / number_of_manufactured_items

        p_ij_n = normalize_p_ij(p_ij, G.nodes)

        C_H = calculate_entropy(G, p_ij_n)

        end_date = datetime.datetime.now().strftime("%Y_%m_%d_")
        filename = "results/" + end_date + "entropy_method_5.txt"
        GraphFile(filename).write_centrality_values_to_file(C_H)


    else:
        print("Method {} does not exist!".format(method))
