# ===================================================================
# ===================================================================
#
# DOT FILE
#
# ===================================================================
# ===================================================================

class DOT_File:
    def __init__(self, fileName, graph_name, graph, property):
        '''Initializes'''
        self.filename = fileName
        self.graph_name = graph_name
        self.dot_file = self._generate_file_content(graph, property)


    def _create_rank(self):
        ''' '''
        rank = '{rank=min; source}\n'
        rank += '{rank=max; sink}'
        return rank


    def _generate_file_content(self, graph, property):
        '''Writes the DOT file'''
        # Data used to create the file
        line0 = {i:'red' for i in range(24)}
        line1 = {i:'green' for i in [24,25]}
        line2 = {i:'blue' for i in [26,27,28]}
        line3 = {i:'yellow' for i in range(29,52)}
        colors = {k: v for d in [line0, line1, line2, line3] for k, v in d.items()}

        # File creation
        file_content = ''
        # General graph info
        file_content += 'digraph ' + self.graph_name + '{\n'
        file_content += 'size = "40,20";\n'
        file_content += 'graph[rankdir=TB, center=true, margin=0.05, nodesep=0.2, ranksep=0.5]\n'
        file_content += 'node[fontname="Courier-Bold", fontsize=14]\n'
        file_content += 'edge[arrowsize=0.2, arrowhead=normal]\n'

        # Nodes
        file_content += 'source [shape=diamond, style=filled, fontsize=20, color=gray, width=2, height=2, fixedsize=true]\n'
        file_content += 'sink [shape=diamond, style=filled, fontsize=20, color=gray, width=2, height=2, fixedsize=true]\n'

        for n in graph.nodes:
            if n not in ['source', 'sink']:
                c = colors.get(n, None)
                p = property.get(n, 0)
                p = ', width=' + str(p) + ', height=' + str(p) + ', fixedsize=true]\n'
                file_content += str(n) + ' [shape=circle, style=filled, fontsize=20, color=' + c + p

        # Edges
        for k,v in graph.edges.items():
            #v = '{:f}'.format(5*v)
            #file_content += str(k[0]) + ' -> ' + str(k[1]) + ' [penwidth=' + v + ']\n'
            file_content += str(k[0]) + ' -> ' + str(k[1]) + ' [penwidth=1]\n'

        # Rank
        file_content += '{rank=source; source}\n'
        file_content += self._create_rank()
        file_content += '{rank=sink; sink}\n'
        file_content += '}'

        return file_content

    def save(self):
        '''Call this method to save dot file contents to .txt file.'''
        path = "figures/" + self.filename
        with open(path, 'w') as f:
            f.write(self.dot_file)
        return True
