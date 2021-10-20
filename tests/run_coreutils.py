from contextlib import redirect_stderr, redirect_stdout
import os
import sys
import pdb
import json
import logging

from progressbar import progressbar

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from bifrost import DotParser, GCC_Utils, ReducibilityDetector

LEVEL = logging.INFO

def setup_loggers(name):
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(LEVEL)


def main(command):
    irreducible = []
    utils = GCC_Utils(pre_args=cmd['pre_args'])
    for dot_file in utils.generate_dot_files(cmd['filename']):
        parser = DotParser(dot_file)
        for graph in parser.graph:
            roots = parser.get_roots(graph)
            if len(roots) < 1:
                print(f"Cannot find roots for {dot_file}")
                continue
            checker = ReducibilityDetector(graph)
            if checker.is_reducible(roots[0]) is False:
                print(f"Irreducible graph in {dot_file}")
                irreducible.append(f"{dot_file}")
    print(irreducible)


if __name__ == '__main__':

    setup_loggers('bifrost.gcc_utils')
    setup_loggers('bifrost.dot_parser')
    setup_loggers('bifrost.reducibility_detector')
    with open("tests/coreutils_commands.json", "r") as f:
        commands = json.load(f)
    
    for cmd in progressbar(commands, redirect_stderr=True, redirect_stdout=True):
        try:
            main(cmd)
        except:
            pdb.set_trace()