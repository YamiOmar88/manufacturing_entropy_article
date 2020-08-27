# Calculate Entropy Centrality from p_ij

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
            p_i[i] += p_ij.get((i,j), 0)

    p_ij_normalized = dict()
    for k,v in p_ij.items():
        i = k[0]
        if p_i[i] != 0:
            p_ij_normalized[k] = v / p_i[i]
        else:
            p_ij_normalized[k] = v

    return p_ij_normalized



def calculate_node_entropy(p_ij, nodes):
    '''Calculate the entropy of node i.
    Input variables:
    xxxx

    Output variables:
    xxxx
    '''
    from math import log

    C_H = {k:0 for k in nodes}
    for i in nodes:
        for j in nodes:
            if p_ij[(i,j)] != 0:
                C_H[i] = C_H[i] + p_ij[(i,j)] * log(p_ij[(i,j)], 2)

    n = len(nodes)
    C_H = {k:-v/log(n,2) for k,v in C_H.items()}
    return C_H
# =============================================================================
# END Function Definitions
# =============================================================================

if __name__ == "__main__":
    # Read data from file
    # ===================
    filename = "2020_08_22_binary_pij_directed_selfloopsonallnodes.txt"

    p_ij, nodes = read_probs_from_file("results/" + filename)

    p_ij_norm = normalize_p_ij(p_ij, nodes)

    C_H = calculate_node_entropy(p_ij_norm, nodes)

    entropy = [(round(v,3),k) for k,v in C_H.items()]
    entropy.sort(reverse=True)

    for item in entropy:
        print("{} & {}\\\\".format(item[1], item[0]))


    # SCC data
    # ========
    from numpy import mean, std
    SCC = [set([39, 40, 41, 43, 44, 45, 47, 48, 49, 50, 51]),
           set([29, 30, 31, 32, 33, 34, 35, 36, 37]),
           set([4, 5, 6, 7, 8, 9, 10, 11]),
           set([16, 17, 18, 19, 20, 21, 22, 23]),
           set([0, 1, 2, 3]),
           set([12, 13, 14, 15]),
           set([24]), set([25]), set([26]), set([27]), set([28]), set([38])]

    SCC_entropy, SCC_stdev = dict(), dict()
    for scc in SCC:
        scc = tuple(scc)
        data = []
        for n in scc:
            data.append(C_H[n])
        SCC_entropy[scc] = mean(data)
        SCC_stdev[scc] = std(data)

    for scc in SCC:
        scc = tuple(scc)
        print("{} & {} & {} & {} \\\\".format(scc, len(scc), round(SCC_entropy[scc],3), round(SCC_stdev[scc],3)))
