import os
import sys
import pdb
import IPython

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from bifrost import DotParser, ReducibilityDetector

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

if __name__ == '__main__':
    test1()
    test2()
