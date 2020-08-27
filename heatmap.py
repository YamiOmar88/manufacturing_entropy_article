# Manufacturing Entropy - Code for the article
# Original Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# This file provides a function to generate a heatmap of  p_ij
# Yamila Mariel Omar
# Date of original code: 23rd July 2020

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
def normalize_row(row):
    '''Normalize row so its sum equals 1.'''
    row_sum = sum(row)
    if row_sum != 0:
        row = [x/row_sum for x in row]
    return(row)


# =============================================================================
def generate_array(nodes, p_ij, normalize=False):
    '''Generate a numpy array from a dictionary of path probabilities.
    Input variables:
    - nodes: set of nodes in the network.
    - p_ij: dictionary of path probabiliites.
    Output variables:
    - np.array of path probabilities.'''

    nodes = list(nodes)
    nodes.sort()

    array = []
    for n in nodes:
        row = []
        for m in nodes:
            row.append( p_ij[(n,m)] )
        if normalize:
            row = normalize_row(row)
        array.append(row)

    return np.array(array)


# =============================================================================
def plot_heatmap(p_ij_array, nodes, title, filename, text, clim_max):
    '''Generate and save heatmap of p_ij.
    Input variables:
    - nodes: set of nodes.
    - p_ij: dictionary of probabilities
    Output variables:
    - Boolean indicating process was completed.'''

    plt.figure(figsize = (10,10), tight_layout=True)
    plt.imshow(p_ij_array, cmap='gnuplot2_r')
    # plt.title(title)
    plt.xlabel("$j$", fontsize=16)
    plt.ylabel("$i$", fontsize=16)
    plt.xticks(np.arange(len(nodes)), nodes, fontsize=8, rotation=90)
    plt.yticks(np.arange(len(nodes)), nodes, fontsize=8)
    plt.colorbar(shrink=0.8)
    plt.clim(0,clim_max)
    plt.text(5, 45, text, fontsize=16)
    plt.savefig(filename)

# =============================================================================
def reduce_p_ij(nodes, p_ij):
    ''' '''
    for i in nodes:
        sum_i = sum([v for k,v in p_ij.items() if k[0] == i])
        if sum_i != 0:
            for j in nodes:
                p_ij[(i,j)] = round(p_ij[(i,j)] / sum_i, 3)

    new_p = dict()
    for i in nodes:
        for j in nodes:
            if p_ij[(i,j)] != 0:
                new_p[(i,j)] = p_ij[(i,j)]

    return new_p

def plot_reduced_heatmap(reduced_p):
    # Get possible values of i and j
    i_set, j_set = set(), set()
    for k in reduced_p.keys():
        i_set.add(k[0])
        j_set.add(k[1])

    i_set = list(i_set)
    i_set.sort()
    j_set = list(j_set)
    j_set.sort()

    # Make array
    array = []
    for i in i_set:
        row = []
        for j in j_set:
            row.append( reduced_p.get((i,j), 0) )
        array.append(row)

    array = np.array(array)

    # plot
    fig, ax = plt.subplots()
    im = ax.imshow(array)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(j_set)))
    ax.set_yticks(np.arange(len(i_set)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(j_set)
    ax.set_yticklabels(i_set)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(i_set)):
        for j in range(len(j_set)):
            if array[i,j] != 0:
                text = ax.text(j, i, array[i, j],
                    ha="center", va="center", color="w", fontsize='xx-small')

    #fig.tight_layout()
    plt.show()
