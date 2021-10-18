import logging
import networkx as nx

logger = logging.getLogger(__name__)


class DotParser(object):
    def __init__(self, dot_file):
        """
        @param dot_file:    The path to the DOT file
        @return A networkx MultiGraph containing the graph in the DOT file
        """
        try:
            self._graph = nx.drawing.nx_pydot.read_dot(dot_file)
            self._filter_graph()
        except FileNotFoundError:
            self._graph = None
            logger.error(f"File {dot_file} not found")
        
    def _filter_graph(self):
        """
        Filter the graph by merging duplicate blocks with the original
        """
        # Roots are identified by 0 incoming edges
        possible_roots = [n for n,d in self.graph.in_degree() if d == 0 ]

        # Duplicate nodes also have 0 incoming edges
        # However, duplicate nodes do not have any instructions
        duplicate_nodes = [n for n in possible_roots if len(self.graph.nodes[n]) == 0 ]

        # Duplicates are identified by following the naming pattern {original}:s[0-9]
        duplicate_node_map = {}
        for tmp in set(possible_roots)-set(duplicate_nodes):
            duplicate_node_map[tmp] = [n for n in duplicate_nodes if n.startswith(tmp) and n[len(tmp)] == ':' ]
        
        # Merge duplicates with original
        for tmp in duplicate_node_map:
            for duplicate_node in duplicate_node_map[tmp]:
                out_edges = list(self.graph.out_edges(duplicate_node))
                for src, dst in out_edges:
                    self.graph.add_edge(tmp, dst)
                    self.graph.remove_edge(src, dst)
                self.graph.remove_node(duplicate_node)
        
    @property
    def graph(self):
        return self._graph
