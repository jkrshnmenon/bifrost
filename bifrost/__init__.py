from .gcc_utils import GCC_Utils
from .dot_parser import DotParser
from .reducibility_detector import ReducibilityDetector

# 1) File parser (DOT to Networkx)  <------------ Done
# 2) File parser (GCC IR to Networkx)
# 3) File parser (Clang IR to Networkx)
# 4) Irreducibility detector  <------------ Done
# 5) Builder (Generate and/or identify DOT files)