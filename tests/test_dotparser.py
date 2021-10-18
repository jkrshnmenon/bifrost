import os
import sys
import pdb
import IPython

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from bifrost import DotParser

def test1():
    parser = DotParser('tests/dotfile_sample.dot')
    assert len(parser.graph) == 1
    graph = parser.graph[0]
    assert graph is not None
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 3
    assert len(DotParser.get_roots(graph)) == 1
    IPython.embed()


def test2():
    parser = DotParser('tests/dotfile_sample_gcc.dot')
    assert len(parser.graph) == 1
    graph = parser.graph[0]
    assert graph is not None
    assert len(graph.nodes) == 7
    assert len(graph.edges) == 8
    assert len(DotParser.get_roots(graph)) == 1


if __name__ == '__main__':
    test1()
    test2()
