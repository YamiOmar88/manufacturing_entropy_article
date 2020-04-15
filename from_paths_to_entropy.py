# Manufacturing Entropy - Code for the article
# Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# Yamila Mariel Omar
# Date of original code: 29th October 2019
# Date of code last modification: 15th April 2020



# ===== Function definitions ============

def remove_i_and_f(edges):
    new_edges = dict()
    for k,v in edges.items():
        if 'i' in k:
            continue
        elif 'f' in k:
            key = (k[0],k[0])
            new_edges[key] = v
        else:
            new_edges[k] = v
    return new_edges

# ===== End Function definitions =========



if __name__ == "__main__":
    # Import needed modules
    from graphfile import GraphFile
    from graph import Graph
    from itertools import product
    import datetime

    # Read necessary data
    filename_paths = "data/manufacturing_paths.txt"
    filename_edges = "data/manufacturing_edges.txt"
    edges = GraphFile(filename_edges).read_edges_from_file()
    paths = GraphFile(filename_paths).read_paths_with_count()

    # Process data
    edges = remove_i_and_f(edges)
    G = Graph(edges)
    G_base = G.nodes

    # Process paths as needed
    all_paths = {(i,j):[] for i,j in product(G_base,G_base)}
    for path,count in paths.items():
        for index in range(len(path)):
            p = path[index:]
            i,j = p[0], p[-1]
            all_paths[(i,j)].append(p)

    for k,v in all_paths.items():
        v = set(v)
        v = [list(x) for x in v]
        all_paths[k] = v

    # Calculate the entropy
    start = datetime.datetime.now()
    G.all_paths = all_paths
    C_H = dict()
    for n in G.nodes:
        node, entropy = G.get_node_entropy(n)
        C_H[node] = entropy
    end = datetime.datetime.now()
    print("Start time: ", start)
    print("End time: ", end)
    print("Run time: ", end-start)

    # Save results to file
    GraphFile("results/_manufacturing_entropy.txt").write_centrality_values_to_file(C_H)
