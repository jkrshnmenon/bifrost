import os
import sys
import pdb
import IPython
from pydot import Dot

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from bifrost import GCC_Utils

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


if __name__ == '__main__':
    test1()
    test2()
    test3()