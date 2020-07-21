# Manufacturing Entropy - Code for the article
# Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# Data used in this file: pre-processed ("data/clean_manufacturing_paths.txt" and "data/clean_manufacturing_edges.txt")
# Yamila Mariel Omar
# Date of original code: 15th April 2020
# Date of code last modification: 21st July 2020

if __name__ == "__main__":
    # Import needed modules
    from graphfile import GraphFile
    from graph import Graph
    from dotfile import DOT_File

    # Read necessary data
    filename_paths = "data/clean_manufacturing_paths.txt"
    paths = GraphFile(filename_paths).read_paths_with_count()

    # Generate edges with dummy source and sink
    edges = dict()
    for k,v in paths.items():
        edges_list = [("source", k[0])] + [(i,j) for (i,j) in zip(k, k[1:])] + [(k[-1], "sink")]
        for edge in edges_list:
            edges[edge] = edges.get(edge, 0) + v

    # Process data
    G = Graph(edges)

    # Full graph
    # ==========
    p = {n: 1 for n in G.nodes}
    dot = DOT_File("manufacturing_network.dot", "Bosch", G, p)
    dot.save()

    # Only above threshold
    # ====================
    number_of_manufactured_items = sum(list(paths.values()))
    threshold = 0.005 * number_of_manufactured_items
    edges = {k:v for k,v in edges.items() if v >= threshold}
    G = Graph(edges)
    p = {n: 1 for n in G.nodes}
    dot = DOT_File("manufacturing_network_05_percent_threshold.dot", "Bosch", G, p)
    dot.save()
