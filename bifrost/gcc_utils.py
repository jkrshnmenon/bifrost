import logging
from typing import List
from os import chdir, getcwd, listdir
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from os.path import exists, expanduser, join
from subprocess import CalledProcessError, check_call

logger = logging.getLogger(__name__)


class GCC_Utils(object):
    def __init__(self, pre_args=[], post_args=[]):
        """
        This class implements most of the utility functions needed to dump the DOT files from GCC.
        @param pre_args:    A list of additional arguments to be passed to GCC before the filename.
        @param post_args:   A list of additional arguments to be passed to GCC after the filename.
        """
        self._fixed_args = ["-fdump-tree-all-graph"]
        self._cc = ["gcc"]
        self._pre_args = pre_args
        self._post_args = post_args
    
    @property
    def pre_args(self):
        return self._pre_args_
    
    @pre_args.setter
    def pre_args(self, new_args: List[str]):
        self._pre_args = new_args
    
    @property
    def post_args(self):
        return self._post_args_
    
    @post_args.setter
    def post_args(self, new_args: List[str]):
        self._post_args = new_args
    
    @contextmanager
    def _create_temp_dir(self):
        with TemporaryDirectory() as dirpath:
            prevdir = getcwd()
            logger.debug(f"Creating temporary directory {dirpath}")
            chdir(expanduser(dirpath))
            yield dirpath
            chdir(prevdir)
            logger.debug(f"Cleaning up temporary directory {dirpath}")
    
    def _do_compile(self, filename):
        cmd = self._cc + self._fixed_args + self._pre_args + [filename] + self._post_args
        if not exists(filename):
            logger.error(f"{filename} does not exist")
            return
        try:
            logger.debug(f"Running command {' '.join(x for x in cmd)}")
            check_call(cmd)
        except CalledProcessError as e:
            logger.error(f"{' '.join(x for x in cmd)} failed with output {e}")
            return

    def iterate_dot_files(self, dirpath):
        """
        Iterate over the dot files inside dirpath.
        """
        for filename in listdir(dirpath):
            if filename.endswith('.dot'):
                logger.debug(f"Found dot file {filename}")
                yield join(dirpath, filename)
    
    def generate_dot_files(self, filename, use_tmpdir=True):
        """
        Compile the filename and return a generator of DOT files.
        Optionally use a temporary directory.
        """
        if use_tmpdir is False:
            self._do_compile(filename)
            for dot_file in self.iterate_dot_files(getcwd()):
                yield dot_file
            return 
        with self._create_temp_dir() as tmpdir:
            self._do_compile(filename)
            for dot_file in self.iterate_dot_files(tmpdir):
                yield dot_file
        
            