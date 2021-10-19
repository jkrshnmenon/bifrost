import os
import sys
import pdb
import logging
import IPython
import networkx

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from bifrost import DotParser, ReducibilityDetector

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

    roots = parser.get_roots(graph)
    assert len(roots) == 1

    checker = ReducibilityDetector(graph)
    flag = checker.is_reducible(roots[0])
    assert flag is True


def test2():
    parser = DotParser('tests/dotfile_sample_gcc.dot')
    assert len(parser.graph) == 1

    graph = parser.graph[0]
    assert graph is not None

    roots = parser.get_roots(graph)
    assert len(roots) == 1

    checker = ReducibilityDetector(graph)
    flag = checker.is_reducible(roots[0])
    assert flag is True


def test3():
    graph = networkx.DiGraph()
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 2)
    graph.add_edge(2, 5)
    graph.add_edge(1, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 1)

    checker = ReducibilityDetector(graph)
    flag = checker.is_reducible(1)
    assert flag is True

def test4():
    graph = networkx.DiGraph()
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(1, 3)
    graph.add_edge(3, 2)

    checker = ReducibilityDetector(graph)
    flag = checker.is_reducible(1)
    assert flag is False

if __name__ == '__main__':
    setup_loggers('bifrost.gcc_utils')
    setup_loggers('bifrost.dot_parser')
    setup_loggers('bifrost.reducibility_detector')
    test1()
    test2()
    test3()
    test4()
