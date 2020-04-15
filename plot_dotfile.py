# Manufacturing Entropy - Code for the article
# Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# Yamila Mariel Omar
# Date of original code: 15th April 2020
# Date of code last modification: 15th April 2020

if __name__ == "__main__":
    # Import needed modules
    from graphfile import GraphFile
    from graph import Graph
    from dotfile import DOT_File

    # Read necessary data
    filename_edges = "data/manufacturing_edges.txt"
    edges = GraphFile(filename_edges).read_edges_from_file()

    # Process data
    G = Graph(edges)

    # Full graph
    # ==========
    p = {n: 1 for n in G.nodes}
    dot = DOT_File("manufacturing_network.dot", "Bosch", G, p)
    dot.save()


    # Graph with only 0.1% or more in edges
    # =====================================
    total_items_produced = 0
    for k,v in edges.items():
        if k[0] == "i":
            total_items_produced += v

    print("Total items produced: ", total_items_produced)

    reduced_edges = {k:v for k,v in edges.items() if v > 0.001 * total_items_produced}
    reduced_G = Graph(reduced_edges)

    dot = DOT_File("reduced_manufacturing_network.dot", "Bosch_reduced", reduced_G, p)
    dot.save()

    # Graph with node size related to entropy
    # =======================================
    C_H = GraphFile("results/manufacturing_entropy.txt").read_centrality_values_from_file()

    dot = DOT_File("reduced_manufacturing_network_entropy_scaled.dot", "Bosch_entropy", reduced_G, C_H)
    dot.save()
