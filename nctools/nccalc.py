# -*- coding: utf-8 -*-

import os
import pyloco

from ncutil import traverse, desc_group, GroupProxy


# TODO: import numpy as np 
# TODO: output should have NCD format too

class NCCalc(pyloco.Task):
    """Read a NCD data file and output numpy-calculated value

'ncmean' task reads a NCD data file and outputs numpy-calculated value

Examples
---------
"""
    _name_ = "nccalc"
    _version_ = "0.1.0"

    def __init__(self, parent):

        self.add_data_argument("data", required=True, help="NCD data")

        self.add_option_argument("-v", "--variable", nargs="+",
                help="namepath to a variable in a NCD data")

        self.add_option_argument("-e", "--eval", dest="calc",
                help="numpy calculation")

        self.register_forward("data", help="value")

    def perform(self, targs):

        data = None

        if isinstance(targs.data, dict):
            data = targs.data

        elif os.path.isfile(targs.data):
            retval, forward = pyloco.perform("ncread", argv=[targs.data])
            data = forward["data"]

        if not isinstance(data, dict):
            raise Exception("Specified input is not correct: %s" % str(targs.data)) 

        mean_function = _mean_method[targs.mean]

        if hasattr(targs, "variable") and targs.variable:
            group = GroupProxy(data)
            outdata = group.apply(targs.path.split("."), mean_function)

        else:
            print("ERROR: No variable is specified by '-v' option")
            sys.exit(-1)

        self.add_forward(data=outdata)
