"""const.py: classes for constant variables"""
__author__      = "Minyoung Kim"
__license__ = "MIT"
__maintainer__ = "Minyoung Kim"
__email__ = "minykim@mit.edu"
__date__ = "07/20/2018"


class NormalizationType(object):
    """Normalization method types"""
    ZERO_AND_ONE = "ranged_zero_and_one"
    MONE_AND_ONE = "ranged_minus_one_and_one"
    ZERO_MEAN = "zero_mean" # ranges vary


class StainChannel(object):
    GFP = "GFP"
    ANTI_GFP = "AntiGFP"
    EGFP_ANTIGFP = "EGFP-AntiGFP"
    GFP_SEG = "GFP_SEG"
    MBP = "MBP"
    AUTOFLUORESCENCE = "AF"
    TOPRO3 = "ToPro3"
    DAPI = "DAPI"
    CY5 = "Cy5"
    CB = "CB"
    PV = "PV"
    IBA1 = "IBA1"
    IBA1_RAW = "IBA1_RAW"
    IBA1_SEG = "IBA1_SEG"
    LECTIN = "Lectin"
    UNKNOWN = "Unknown"
    UNKNOWN_SEG = "Unknown_SEG"
    UNKNOWN_SEG_GB = "Unknown_SEG_GB"
    UNKNOWN_SEG_GB_THR = "Unknown_SEG_GB_THR"
    V5 = "V5"
    V5_SEG = "V5_SEG"
    V5_SEG_GB = "V5_SEG_GB"
    V5_SEG_GB_THR = "V5_SEG_GB_THR"
    CFOS = "cFos"
    TDTOMATO = "tdTomato"

