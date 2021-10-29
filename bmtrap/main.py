"""main.py: Main entry point"""
__author__      = "Minyoung Kim"
__license__ = "MIT"
__maintainer__ = "Minyoung Kim"
__email__ = "minykim@mit.edu"

import sys
import os
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import numpy as np
import argparse

from bmtrap.params import BaseParams
from bmtrap.coreg import coReg


def main():
    p = BaseParams()
    p.build(sys.argv, "TRAP Parser")
    cr = coReg(p)

    print("loading data...")
    cr.load_data()
    print("==== DATA ====")
    print("\tsrc vol shape: ", cr.src_vol.shape)
    print("\tdst vol shape: ", cr.dst_vol.shape)
    print("\tdst probMap shape: ", cr.dst_probs.shape)
    print("\tlen(src_cc): ", len(cr.src_cc))

    print("finding co-positive cells..")
    cp_ccl = cr.find_coPos(viz=False, save=True)


if __name__=="__main__":
    main()
