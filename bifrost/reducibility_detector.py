from networkx import dfs_preorder_nodes
from networkx.algorithms.dominance import immediate_dominators


class ReducibilityDetector(object):
    def __init__(self, graph):
        self._graph = graph
    
    @property
    def graph(self):
        return self._graph

    def generate_dom_info(self, root):
        imm_dom_info = immediate_dominators(self.graph, root)
        dom_info = {}
        for node in imm_dom_info:
            dom_info[node] = set()
            dom_info[node].add(node)
            tmp = imm_dom_info[node]
            while tmp not in dom_info[node]:
                dom_info[node].add(tmp)
                tmp = imm_dom_info[tmp]

        return dom_info
    
    def search(self, node, visited_map, dfn_info):
        visited_map[node] = True
        for succ in self.graph.successors(node):
            if visited_map[succ] is False:
                self.search(succ, visited_map, dfn_info)
        dfn_info[node] = self.ctr
        self.ctr -= 1


    def generate_dfn_info(self, root):
        self.ctr = len(self.graph.nodes)
        visited_map = {x: False for x in self.graph.nodes}
        dfn_info = {}
        self.search(root, visited_map, dfn_info)
        return dfn_info

    def find_back_edges(self, dom_info):
        back_edges = []
        for edge in self.graph.edges:
            if len(edge) > 2:
                u,v = edge[:2]
            else:
                u,v = edge
            # If v dominates u, this is a back edge
            if v in dom_info[u]:
                back_edges.append((u,v))
        
        return back_edges

    def find_retreating_edges(self, dfn_info):
        retreating_edges = []
        for edge in self.graph.edges:
            if len(edge) > 2:
                u,v = edge[:2]
            else:
                u,v = edge
            # If dfn[u] >= dfn[v], this is a retreating edge
            if dfn_info[u] >= dfn_info[v]:
                retreating_edges.append((u,v))
        
        return retreating_edges

    def is_reducible(self, root: str) -> bool:
        """
        Algorithm:
        1) Generate dominator information for every node in graph
        2) Generate depth-first-numbers(dfn) for every node in graph
        3) Find back edges in the graph (Edge (u,v) is back edge if v dominates u)
        4) Find retreating edges in the graph (Edge (u,v) is retreating if dfn[u] >= dfn[v])
        5) Iterate through every retreating edge and check if it is a back edge.
        6) If any retreating edge is not a back edge, graph is irreducible
        """
        dom_info = self.generate_dom_info(root)
        dfn_info = self.generate_dfn_info(root)
        back_edges = self.find_back_edges(dom_info)
        retreating_edges = self.find_retreating_edges(dfn_info)

        flag = True
        for (u,v) in retreating_edges:
            if (u,v) not in back_edges:
                flag = False
                break

        return flag