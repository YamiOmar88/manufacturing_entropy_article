# Manufacturing Entropy - Code for the article
# Original Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# Data used in this file: pre-processed ("data/manufacturing_paths.txt" and "data/manufacturing_edges.txt")
# Yamila Mariel Omar
# Date of original code: 21st July 2020

from graphfile import GraphFile


# Load manufacturing paths paths
# ==============================
paths = GraphFile("data/manufacturing_paths.txt").read_paths_with_count()
number_of_manufactured_items = sum(paths.values())

# Load edges
# ==========
edges = GraphFile("data/manufacturing_edges.txt").read_edges_from_file()

# Filter out edges that only serve a handfull of items
# ====================================================
threshold = 0.001 * number_of_manufactured_items
edges_to_remove = [k for k,v in edges.items() if v < threshold]
edges_to_remove = set(edges_to_remove)

# Clean manufacturing paths
# =========================
clean_paths = {}
for k,v in paths.items():
    e = [(i,j) for (i,j) in zip(k, k[1:])]
    e = set(e)
    if len(edges_to_remove.intersection(e)) == 0:
        clean_paths[k] = clean_paths.get(k, 0) + v

# Get clean edges
# ===============
clean_edges = {}
for k,v in clean_paths.items():
    e = [(i,j) for (i,j) in zip(k, k[1:])]
    for edge in e:
        clean_edges[edge] = clean_edges.get(edge, 0) + v

# Save clean paths and edges
# ==========================
GraphFile("data/clean_manufacturing_paths.txt").write_paths_with_count(clean_paths)
GraphFile("data/clean_manufacturing_edges.txt").write_graph_to_file(clean_edges)
