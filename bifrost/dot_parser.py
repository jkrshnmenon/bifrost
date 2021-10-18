import logging
import networkx
from typing import List
from os.path import exists
from pydot import graph_from_dot_file
from networkx.drawing.nx_pydot import read_dot, from_pydot

logger = logging.getLogger(__name__)


class DotParser(object):
    def __init__(self, dot_file : str) -> None:
        """
        @param dot_file:    The path to the DOT file
        @return A list of networkx MultiGraphs containing the graphs in the DOT file
        """
        if exists(dot_file):
            self._parse_dot_file(dot_file)
        else:
            self._graph = []
            logger.error(f"File {dot_file} not found")
    
    def _parse_dot_file(self, path: str) -> None:
        graph = read_dot(path)

        if len(graph.nodes) > 0:
            self._graph = [self._filter_graph(graph)]
            return
        
        # handle subgraphs
        pydot_graph = graph_from_dot_file(path)
        self._graph = []
        for p in pydot_graph:
            for subgraph in p.get_subgraphs():
                graph = from_pydot(subgraph)
                self._graph.append(self._filter_graph(graph))

        
    def _filter_graph(self, graph: networkx.MultiGraph) -> networkx.MultiGraph:
        """
        Filter the graph by merging duplicate blocks with the original
        """
        # Roots are identified by 0 incoming edges
        possible_roots = [n for n,d in graph.in_degree() if d == 0 ]
        possible_exits = [n for n,d in graph.out_degree() if d == 0 ]

        # Duplicate nodes also have 0 incoming edges
        # However, duplicate nodes do not have any instructions
        duplicate_nodes = [n for n in possible_roots if len(graph.nodes[n]) == 0 ]

        # Duplicates are identified by following the naming pattern {original}:s[0-9]
        duplicate_node_map = {}
        for tmp in set(possible_roots)-set(duplicate_nodes):
            duplicate_node_map[tmp] = [n for n in duplicate_nodes if n.startswith(tmp) and n[len(tmp)] == ':' ]
        
        # Merge duplicates with original
        for tmp in duplicate_node_map:
            for duplicate_node in duplicate_node_map[tmp]:
                out_edges = list(graph.out_edges(duplicate_node))
                for src, dst in out_edges:
                    graph.add_edge(tmp, dst)
                    graph.remove_edge(src, dst)
                graph.remove_node(duplicate_node)

        duplicate_nodes = [n for n in possible_exits if len(graph.nodes[n]) == 0 ]

        duplicate_node_map = {}
        for tmp in set(possible_exits)-set(duplicate_nodes):
            duplicate_node_map[tmp] = [n for n in duplicate_nodes if n.startswith(tmp) and n[len(tmp)] == ':' ]
        
        for tmp in duplicate_node_map:
            for duplicate_node in duplicate_node_map[tmp]:
                in_edges = list(graph.in_edges(duplicate_node))
                for src, dst in in_edges:
                    graph.add_edge(src, tmp)
                    graph.remove_edge(src, dst)
                graph.remove_node(duplicate_node)
        
        flag = False
        for (u,v,_) in graph.edges:
            if 'label' in graph.nodes[u] and graph.nodes[u]['label'].strip("'").strip('"') == 'ENTRY':
                if 'label' in graph.nodes[v] and graph.nodes[v]['label'].strip("'").strip('"') == 'EXIT':
                    flag = True
                    break
        
        if flag is True:
            graph.remove_edge(u,v)
        
        return graph
        
    @property
    def graph(self) -> List[networkx.MultiGraph]:
        return self._graph

    @staticmethod
    def get_roots(graph) -> List[str]:
        return [n for n,d in graph.in_degree() if d == 0 ]