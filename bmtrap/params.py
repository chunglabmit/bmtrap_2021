"""params.py: Parameter Parser"""
__author__      = "Minyoung Kim"
__license__ = "MIT"
__maintainer__ = "Minyoung Kim"
__email__ = "minykim@mit.edu"

import argparse
import bmtrap.util as tUtil

class BaseParams(object):
    """BaseParams Class"""

    def __init__(self):
        self.debug = False
        self.viz = False

    def _parser(self, desc=None):
        """add list of arguments to ArgumentParser
           : This is a placeholder for subclasses

        Params
        ---------
        desc: description of Params set
        """
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument('-st', '--src_tifpath', default=None,
                            help='Path to source TIFF')
        parser.add_argument('-sz', '--src_zarrpath',
                            help="Path to source ZARR", required=True)
        parser.add_argument('-sc', '--src_cc',
                            help="NUMPY file containing source cell coordinates",
                            required=True)
        parser.add_argument('-dt', '--dst_tifpath', default=None,
                            help='Path to destination TIFF')
        parser.add_argument('-dz', '--dst_zarrpath',
                            help='Path to destination ZARR', required=True)
        parser.add_argument('-dp', '--dst_probpath',
                            help="Path to destination Probability Map", required=True)
        parser.add_argument('-sp', '--save_path',
                            help="Path to save output files", required=True)
        parser.add_argument('-thr', '--threshold', type=float, default=0.4,
                            help="Threshold for co-positivity", required=True)
        parser.add_argument('-dbg', '--debug', action='store_true', default=False)

        return parser

    def build(self, argv, desc, returnOnly=False):
        """parse arguments

        Params
        ---------
        argv: parameter arguments from command line
        desc: description of the Params set
        """

        # parse
        parser = self._parser(desc)
        args = parser.parse_args(argv[1:])
        args_dict = vars(args)

        # update class variables with args passed
        vars(self).update(args_dict)

        # placeholder function for arguments post-processing
        self.postproc_args()

        # print if needed
        if self.debug:
            self.print_params(returnOnly)


    def postproc_args(self):
        # Nothing to do for base class
        pass


    def print_params(self, returnOnly=False):
        """print class parameters in a nice format"""
        return tUtil.print_class_params(self.__class__.__name__, vars(self), returnOnly=returnOnly)


