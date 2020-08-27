# Plot heatmap and save

from heatmap import *
import os

# =============================================================================
# Function Definitions
# =============================================================================
def read_probs_from_file(filename):
    ''' '''
    p_ij = dict()
    nodes = set()
    with open(filename) as f:
        for line in f:
            try:
                line = line.strip().split(" ")
                i, j, p = int(line[0]), int(line[1]), float(line[2])
                p_ij[(i,j)] = p
                nodes.add(i)
                nodes.add(j)
            except:
                print(line)
    return p_ij, nodes


# =============================================================================
# END Function Definitions
# =============================================================================

if __name__ == "__main__":
    # Read data from file
    # ===================
    print("Available files:")
    files = os.listdir("results/")
    files = [f for f in files if "_pij_" in f]
    for f in files:
        print(f)

    filename = input("\n\nSelected File:")
    normalize = input("\nDo you wish to normalize (y/n)? ")

    p_ij, nodes = read_probs_from_file("results/" + filename)
    nodes = list(nodes)
    nodes.sort()

    # Make plot and save
    # ==================
    fn = filename[:11] + "heatmap_"
    # Normalize if needed
    if normalize == "y":
        p_ij_array = generate_array(nodes, p_ij, normalize=True)
        clim_max = round(np.quantile(p_ij_array, 0.999),1)
        title = "normalized $p_{ij}$"
        fn = fn + "norm_pij_"
    else:
        p_ij_array = generate_array(nodes, p_ij, normalize=False)
        clim_max = 1
        title = "not normalized $p_{ij}$"
        fn = fn + "pij_"

    # Binary or weighted
    if "_binary_" in filename:
        text =  "Binary, directed graph\n"
        fn = fn + "binary_"
    elif "_weighted_" in filename:
        text = "Weighted, directed graph\n"
        fn = fn + "weighted_"

    # Self-loops where?
    if "_selfloopsonallnodes" in filename:
        text = text + "with self-loops on all nodes"
        fn = fn + "selfloopsonallnodes"
    elif "_selfloopsonendnodesonly" in filename:
        text = text + "with self-loops on end nodes only"
        fn = fn + "selfloopsonendnodesonly"

    text = text + "\n" + title
    title = "$p_{ij}$"

    filename = "figures/" + fn + ".pdf"

    plot_heatmap(p_ij_array, nodes, title, filename, text, clim_max)
