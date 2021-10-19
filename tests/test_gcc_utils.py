import os
import sys
import pdb
import json
import logging
import IPython
from pydot import Dot

LEVEL = logging.ERROR

def setup_loggers(name):
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(LEVEL)

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from bifrost import GCC_Utils, DotParser, ReducibilityDetector

def test1():
    utils = GCC_Utils()
    filename = "/home/sefcom/projects/decompiler/bifrost/tests/test1.c"
    assert len(list(utils.generate_dot_files(filename))) == 15


def test2():
    utils = GCC_Utils()
    filename = "/home/sefcom/projects/decompiler/bifrost/tests/test2.c"
    assert len(list(utils.generate_dot_files(filename))) == 15


def test3():
    utils = GCC_Utils()
    filename = "./tests/test1.c"
    assert len(list(utils.generate_dot_files(filename))) == 0


def test4():
    with open("tests/coreutils_commands.json", "r") as f:
        data = json.load(f)
    
    cmd = data[0]
    utils = GCC_Utils(pre_args=cmd['pre_args'])
    assert len(list(utils.generate_dot_files(cmd['filename']))) > 0


def test5():
    with open("tests/coreutils_commands.json", "r") as f:
        data = json.load(f)
    
    cmd = data[0]
    utils = GCC_Utils(pre_args=cmd['pre_args'])
    for file in utils.generate_dot_files(cmd['filename']):
        parser = DotParser(file)
        for graph in parser.graph:
            roots = parser.get_roots(graph)
            checker = ReducibilityDetector(graph)
            checker.is_reducible(roots[0])
            break
        break


if __name__ == '__main__':
    setup_loggers('bifrost.gcc_utils')
    setup_loggers('bifrost.dot_parser')
    setup_loggers('bifrost.reducibility_detector')

    test1()
    test2()
    test3()
    test4()
    test5()