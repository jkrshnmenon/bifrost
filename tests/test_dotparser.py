import os
import sys
import pdb
import IPython

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

import bifrost


if __name__ == '__main__':
    parser = bifrost.DotParser('tests/dotfile_sample.dot')
    assert parser.graph is not None
    assert len(parser.graph.nodes) == 3
    assert len(parser.graph.edges) == 3

