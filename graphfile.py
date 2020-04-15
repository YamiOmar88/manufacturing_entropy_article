# Useful functions
# Author: Yamila M. Omar
# Date: 4/4/2019
# ======================

class GraphFile:
    def __init__(self, fileName):
        '''Initialize class with name of file.'''
        self.filename = fileName


    def read_edges_from_file(self):
        '''Read graph from file. The file contains one edge (i,j)
        and its weight w_ij per line as follows:
        i j w_ij'''
        edges = {}
        with open(self.filename) as fileHandle:
            for line in fileHandle:
                line = line.strip().split()
                if len(line) != 3: continue
                i, j, w_ij = line[0], line[1], line[2]

                try:
                    i = int(i)
                except ValueError:
                    pass

                try:
                    j = int(j)
                except ValueError:
                    pass

                w_ij = int(w_ij)
                edges[(i,j)] = w_ij

        return edges



    def write_graph_to_file(self, G):
        '''Write graph G to file. G must be a dictionary.
        Keys are tuples (i,j) of edges and values are weights w_ij.'''
        with open(self.filename, 'w') as f:
            for k,v in G.items():
                i, j, w_ij = str(k[0]), str(k[1]), str(v)
                f.write(i + ' ' + j + ' ' + w_ij + '\n')
        return True



    def read_centrality_values_from_file(self):
        '''Read centrality values from file. The file must contain
        one node per line and its centrality value as follows:
        i c_i'''
        C = {}
        with open(self.filename) as f:
            for line in f:
                line = line.strip().split()
                i, c_i = line[0], float(line[1])

                try:
                    i = int(i)
                except ValueError:
                    pass

                C[i] = c_i
        return C



    def write_centrality_values_to_file(self, C):
        '''Write centrality values to file. C must be a dictionary.
        Keys are nodes i and values are centrality values c_i.'''
        with open(self.filename, 'w') as f:
            for k,v in C.items():
                i, c_i = str(k), str(v)
                f.write(i + ' ' + c_i + '\n')
        return True


    def write_paths_to_file(self, paths_list):
        '''Write a list of paths to file. paths_list must be a list of paths.
        Each individual path is saved in a different line.'''
        with open(self.filename, 'w') as f:
            for p in paths_list:
                p = [str(n) for n in p]
                s = ' '.join(p)
                f.write(s + '\n')
        return True



    def read_paths_from_file(self):
        '''Read paths from file. They must be saved in the format given by
        the write_paths_to_file method.'''
        with open(self.filename) as f:
            all_paths = dict()
            for line in f:
                line = line.strip().split(' ')
                line = [int(x) for x in line]
                i, j = line[0], line[-1]
                all_paths[(i,j)] = all_paths.get((i,j), [])
                all_paths[(i,j)].append(line)
        return all_paths


    def read_paths_with_count(self):
        '''Read paths from file with count values. The file must contain one
        path per line as nodes separated with whitespace and the last value is
        the count. Example:
        1 2 3 4 5 6 1000 '''
        with open(self.filename) as f:
            all_paths = dict()
            for line in f:
                line = line.strip().split(' ')
                line = [int(x) for x in line]
                path, count = tuple(line[0:-1]), line[-1]
                all_paths[path] = all_paths.get(path, 0) + count
        return all_paths


    def write_paths_with_count(self, paths_with_count_dict):
        '''Write paths to file with count values. The file will contain one
        path per line as nodes separated with whitespace and the last value is
        the count. Example:
        1 2 3 4 5 6 1000 '''
        with open(self.filename, 'w') as f:
            for path,count in paths_with_count_dict.items():
                line = [str(n) for n in path] + [str(count)]
                line = ' '.join(line)
                f.write(line + '\n')
        return True
