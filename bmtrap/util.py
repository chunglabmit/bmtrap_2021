"""util.py: util functions"""
__author__      = "Minyoung Kim"
__license__ = "MIT"
__maintainer__ = "Minyoung Kim"
__email__ = "minykim@mit.edu"


#----------
# imports
#----------
import os
from os import system
from os.path import *
from datetime import datetime
import json

def dump2json(fname, data):
    """dump data to json
    :param fname: JSON file name to save
    :param data: data (list) to save
    """
    with open(fname, 'w') as fp:
        json.dump(data, fp, indent=2)


def print_class_params(class_name, class_vars, only=None, exclude=None, returnOnly=False):
    """print class parameters in a nice format

    Parameters
    ----------
    class_name: string
        name of the class
    class_var: Class Variable Object
        list of tuples of variable name and value
    only: list
        return only variables specified
    exclude: list
        return variables except for specified
    """

    p = PRT()
    items = sorted(class_vars.items())
    filtered = []

    for item in items:
        if only is not None:
            if item[0] not in only:
                continue

        if exclude is not None:
            if item[0] in exclude:
                continue

        filtered.append(item)


    entry = '\n'.join("[ %s ]\t: %s" % item for item in items)
    title_b = "[---------- %s() Variables and their values (BEGIN) ----------]"%class_name
    title_e = "[---------- %s() Variables and their values (END) ----------]"%class_name

    if not returnOnly:
        p.p(title_b, p.LOG)
        p.p("{}".format(entry), p.LOG)
        p.p(title_e, p.LOG)

    return title_b, entry, title_e


##----------------------------------------------------------
# CLASS PRT()
# - print message to terminal with colors different by level
#-----------------------------------------------------------
class PRT(object):
    STATUS = "status-progress"
    STATUS2 = "status-progress-less-important"
    ERROR = "error"
    WARNING = "warning"
    LOG = "log"
    LOGW = "logw"
    FLAGS = {
             STATUS:'#00af00',       # Green3
             STATUS2: '#0087ff',     # DodgerBlue1
             ERROR:'#d70000',        # Red3
             WARNING:'#ff5f00',      # OrangeRed1
             LOG:'#4e4e4e',          # Grey30
             LOGW:'#cecece'          # Brighter Grey
            }

    def __init__(self):
        pass

    @staticmethod
    def p(_msg, _flag):
        if _flag not in PRT.FLAGS.keys():
            print("INVALID FLAG for PRT_MSG()!%s"%(_flag))
            exit(1)
        print("%s"%(_msg))


def get_current_time():
    """return current time"""
    return datetime.now().strftime('%Y-%m-%d_%H%M%S')
