# Entropy Centrality
# Author: Yamila M. Omar
# Date: 5/4/2019
from math import log

class Graph:
    def __init__(self, edges=dict()):
        '''Initializes a Graph. Variables:
            - edges: dictionary with edge tuples as keys (i,j) and
            weight w_ij as values.'''
        self.edges = edges
        self.nodes = self._get_set_of_nodes()
        self.downstream_nodes = self._get_downstream_nodes()
        self.all_paths = {}


    def _get_set_of_nodes(self):
        '''Find the nodes from the edges.'''
        edges = list(self.edges.keys())
        nodes = [i[0] for i in edges] + [i[1] for i in edges]
        return set(nodes)


    def addEdge(self, i, j, w_ij):
        '''Allows to add and edge (i,j) and its weight w_ij to the graph'''
        self.edges[(i,j)] = w_ij


    def deleteEdge(self, i, j):
        '''Allows to delete an edge (i,j) and its associated weight'''
        try:
            self.edges.pop((i,j))
        except KeyError:
            print("{0} cannot be deleted. {0} in Graph.".format((i,j)))


    def normalize(self):
        '''This function allows to set edge weights in a 0 to 1 scale.'''
        totSum = 0
        for k,v in self.edges.items():
            if k[0] == 'i':
                totSum += v
        normalized_edges = {}
        for k,v in self.edges.items():
            normalized_edges[k] = round(v/totSum, 5)
        return normalized_edges


    def _remove_edges_below_tolerance(self, edges, tolerance):
        '''This function is used by remove_underutilized_edges and should
        not be called by users. It takes two input variables:
        - edges: dictionary with tuples of edges (i,j) as keys,
        - tolerance: and integer or float used to filter out edges.
        The function returns a new dictionary of edges.'''
        new_dict = {}
        for k,v in edges.items():
            if v >= tolerance:
                new_dict[k] = v
        return new_dict


    def remove_underutilized_edges(self, tolerance, normalize=False):
        ''' This function removes edges whose weight is below a tolerance.
        Input variables:
        - tolerance (integer or float) used to filter out edges,
        - normalize (default value False) whether the weighted edges are to
        be normalized.
        The function returns a dictionary of edges.'''
        if normalize:
            normalized_edges = self.normalize()
            return self._remove_edges_below_tolerance(normalized_edges, tolerance)
        else:
            return self._remove_edges_below_tolerance(self.edges, tolerance)


    def _get_downstream_nodes_of_i(self, i):
        '''This function finds the downstream neighbours of node i.'''
        downstream_nodes_of_i = list()
        for edge in self.edges.keys():
            u, v = edge[0], edge[1]
            if u == i: downstream_nodes_of_i.append(v)
        downstream_nodes_of_i = set(downstream_nodes_of_i)
        return list(downstream_nodes_of_i)


    def _get_downstream_nodes(self):
        '''This function returns the downstream nodes of each node in the
        graph. It is used to assign this value to an attribute.'''
        downtream_nodes = dict()
        for n in self.nodes:
            downtream_nodes[n] = self._get_downstream_nodes_of_i(n)
        return downtream_nodes


    def searchPaths(self, i, j, visited, path):
        '''Searches all possible paths from node i to node j.'''
        # Set current node as visited and store it in path
        visiting = dict(visited)
        visiting[i] = True
        aux = list(path)
        aux.append(i)
        # If current node is not same as destination, recursively
        # search adjacent nodes.
        all_paths = []
        if i != j:
            for u in self.downstream_nodes[i]:
                if visiting[u] == False:
                    all_paths += self.searchPaths(u, j, visiting, aux)
        else:
            all_paths += [aux[:]]
        return all_paths

    def findAllPaths(self, i, j):
        '''Find all possible paths from node i to node j.'''
        # Set all nodes as not visited
        visited = {n: False for n in self.nodes}
        # Create a list to store the path
        path = []
        # Call recursive function to search for paths
        return self.searchPaths(i, j, visited, path)


    def find_paths_and_log(self, i, j):
        '''This function allows to log all paths. It calls findAllPaths(i,j)
        to search for the paths but adds the option to log.
        IMPORTANT: The logging must be configured on the main script. Here is a
        suggested example to add to main:

        import logging
        logging.basicConfig(filename="mylog.log", level=logging.INFO, format='%(asctime)s === %(message)s')
        '''
        import logging
        paths_i_to_j = self.findAllPaths(i, j)
        for path in paths_i_to_j:
            logging.info("i=%s j=%s path=%s", i, j, path)
        return True


    def _downstream_degree(self, t, path):
        '''Determine the downstream degree of t. Input variables:
        - node t for which the downstream degree is required,
        - path in which this downstream degree is to be calculated.
        The function returns the downstream degree of node t as
        defined by Tutzauer (2007). The function is generalized to
        also work with weighted graphs.'''
        downstream_degree = 0
        t_index = path.index(t)
        for adj_node in self.downstream_nodes[t]:
            if adj_node not in path[:t_index]:
                downstream_degree += self.edges[ (t, adj_node) ]
        return downstream_degree


    def _transfer_probability(self, t, path):
        '''Determine the transfer probability of path k. Input variables:
        - node t for which the transfer probability is required,
        - path in which this transfer probability is to be calculated.
        The function returns the transfer probability of node t as
        defined by Tutzauer (2007). The function is generalized to
        also work with weighted graphs.'''
        D_t = self._downstream_degree(t, path)
        if D_t == 0:
            T_k = 0
        else:
            t_index = path.index(t)
            edge =  (t, path[t_index + 1])
            T_k = self.edges.get(edge, 0) / D_t
        return T_k

    def _stopping_probability(self, t, path):
        '''Determine the stopping probability of path k. Input variables:
        - node t for which the stopping probability is required,
        - path in which this stopping probability is to be calculated.
        The function returns the stopping probability of node t as
        defined by Tutzauer (2007). The function is generalized to
        also work with weighted graphs. In order to work for looped
        graphs, the edge (t,t) must explicitly show up in self.edges!'''
        D_t = self._downstream_degree(t, path)
        if D_t == 0:
            sigma_k = 1
        else:
            edge = (t, t)
            sigma_k = self.edges.get(edge, 0) / D_t
        return sigma_k

    def _probability_path_ij(self, i, j):
        '''Calculate the probability of path i -> j. This is done
        following the general formulae on Tutzauer (2007).'''
        prob_ij = 0
        if self.all_paths.get((i,j), None) == None:
            self.all_paths[(i,j)] = self.findAllPaths(i, j)
        for path in self.all_paths[(i,j)]:
            product = 1
            for node in path[:-1]:
                T_k = self._transfer_probability(node, path)
                product = product * T_k
            product = product * self._stopping_probability(j, path)
            prob_ij += product
        return prob_ij


    def get_node_entropy(self, i):
        '''Calculate the entropy of node i. The function returns
        a tuple (i, C_H) of node i and its entropy.'''
        C_H = 0
        for j in self.nodes:
            p_ij = self._probability_path_ij(i, j)
            if p_ij != 0: C_H = C_H + p_ij * log(p_ij, 2)
        C_H = - C_H
        return (i, C_H)

    def get_node_entropy_and_print(self, i):
        print(self.get_node_entropy(i))



    @property
    def adjacencyList(self):
        '''Returns the adjacency list.'''
        ingoing, outgoing = {k:[] for k in self.nodes}, {k:[] for k in self.nodes}
        for edge in self.edges.keys():
            i, j = edge[0], edge[1]
            outgoing[i] = outgoing.get(i, []) + [j]
            ingoing[j] = ingoing.get(j, []) + [i]
        ingoing = {k:set(v) for k,v in ingoing.items()}
        outgoing = {k:set(v) for k,v in outgoing.items()}
        return ingoing, outgoing


    @property
    def degree(self):
        '''Calculate the degree of each node.'''
        ingoing, outgoing = self.adjacencyList
        inDegree = {k:len(ingoing[k]) if k in ingoing else 0 for k in self.nodes}
        outDegree = {k:len(outgoing[k]) if k in outgoing else 0 for k in self.nodes}
        return inDegree, outDegree


    @property
    def strength(self):
        '''Calculate the strength of each node.'''
        inStrength, outStrength = {k:0 for k in self.nodes}, {k:0 for k in self.nodes}
        for edge,weight in self.edges.items():
            i, j = edge[0], edge[1]
            inStrength[j] = inStrength[j] + weight
            outStrength[i] = outStrength[i] + weight
        return inStrength, outStrength

    @property
    def entropyCentrality(self):
        '''Calculate the entropy of each node.'''
        C_H = {k:0 for k in self.nodes}
        for i in self.nodes:
            for j in self.nodes:
                p_ij = self._probability_path_ij(i, j)
                if p_ij != 0: C_H[i] = C_H[i] + p_ij * log(p_ij, 2)
            C_H[i] = - C_H[i]
        return C_H
