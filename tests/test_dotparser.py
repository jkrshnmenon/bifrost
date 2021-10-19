import os
import sys
import pdb
import logging
import IPython
from pydot import Dot

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from bifrost import DotParser

LEVEL = logging.ERROR

def setup_loggers(name):
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(LEVEL)

def test1():
    parser = DotParser('tests/dotfile_sample.dot')
    assert len(parser.graph) == 1
    graph = parser.graph[0]
    assert graph is not None
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 3
    assert len(DotParser.get_roots(graph)) == 1


def test2():
    parser = DotParser('tests/dotfile_sample_gcc.dot')
    assert len(parser.graph) == 1
    graph = parser.graph[0]
    assert graph is not None
    assert len(graph.nodes) == 7
    assert len(graph.edges) == 7
    assert len(DotParser.get_roots(graph)) == 1


def test3():
    parser = DotParser('tests/multiple_graphs.dot')
    assert len(parser.graph) == 2
    G1, G2 = parser.graph
    assert G1 is not None and G2 is not None
    assert len(G1.nodes) == 7
    assert len(G2.nodes) == 7
    assert len(G1.edges) == 7
    assert len(G2.edges) == 7
    assert len(DotParser.get_roots(G1)) == 1
    assert len(DotParser.get_roots(G2)) == 1


if __name__ == '__main__':
    setup_loggers('bifrost.gcc_utils')
    setup_loggers('bifrost.dot_parser')
    setup_loggers('bifrost.reducibility_detector')
    test1()
    test2()
    test3()
