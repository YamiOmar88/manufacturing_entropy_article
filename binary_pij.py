# Manufacturing Entropy - Code for the article
# Original Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# Data used in this file: pre-processed ("data/clean_manufacturing_edges.txt")
# Yamila Mariel Omar
# Date of original code: 17th August 2020
# Date of code last modification: 17th August 2020


# ===== Function definitions ============

def add_self_loops(paths, edges):
    for k,v in paths.items():
        self_loop = (k[-1], k[-1])
        edges[self_loop] = edges.get(self_loop, 0) + v
    return edges

# ======= END Function Defs ===============



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

    # =========================================================================
    # CALCULATE ENTROPY
    # =========================================================================
    if method == 1:
        # Method 1: binary, directed graph with self-loops on all nodes
        # Due to computation issues, this is deployed in an HPC!!!
        # =============================================================
        edges = {k:1 for k,v in edges.items()}
        G = Graph(edges)

        nodes = G.nodes
        for n in G.nodes:
            G.addEdge(n, n, 1)

        # Check that all edges have a value of 1
        assert len(set(G.edges.values())) == 1

        print("\nNumber of nodes: ", len(G.nodes))
        print("Number of edges: ", len(G.edges.keys()))

        print("Binary, directed graph with self-loops on all nodes\n")
        pool = multiprocessing.Pool()
        start = datetime.datetime.now()
        input_variables = zip(G.nodes, ["Tutzauer"]*len(G.nodes))
        print("Start time: ", start)
        r = pool.starmap(G._probability_paths_from_i, input_variables)
        end = datetime.datetime.now()
        print("End time: ", end)
        print("Run time: ", end - start)
        pool.close()
        pool.join()

        p_ij = {k:v for d in r for k,v in d.items()}

        end_date = end.strftime("%Y_%m_%d_")
        filename = "results/" + end_date + "binary_pij_directed_selfloopsonallnodes.txt"
        GraphFile(full_path + filename).write_graph_to_file(p_ij)



    elif method == 2:
        # Method 2: binary, directed graph with self-loops only on end nodes
        # Due to computation issues, this is deployed in an HPC!!!
        # ==================================================================
        edges = add_self_loops(paths, edges)
        edges = {k:1 for k,v in edges.items()}
        G = Graph(edges)

        # Check that all edges have a value of 1
        assert len(set(G.edges.values())) == 1

        print("\nNumber of nodes: ", len(G.nodes))
        print("Number of edges: ", len(G.edges.keys()))

        print("Binary, directed graph with self-loops on end nodes only\n")
        pool = multiprocessing.Pool()
        start = datetime.datetime.now()
        input_variables = zip(G.nodes, ["Tutzauer"]*len(G.nodes))
        print("Start time: ", start)
        r = pool.starmap(G._probability_paths_from_i, input_variables)
        end = datetime.datetime.now()
        print("End time: ", end)
        print("Run time: ", end - start)
        pool.close()
        pool.join()

        p_ij = {k:v for d in r for k,v in d.items()}

        end_date = end.strftime("%Y_%m_%d_")
        filename = "results/" + end_date + "binary_pij_directed_selfloopsonendnodesonly.txt"
        GraphFile(full_path + filename).write_graph_to_file(p_ij)

    else:
        print("Method {} does not exist!".format(method))
