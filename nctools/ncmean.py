# -*- coding: utf-8 -*-

import os
import pyloco

from ncutil import traverse, desc_group, GroupProxy

def arithmetic_mean(var):
    import pdb; pdb.set_trace()

def geometric_mean(var):
    import pdb; pdb.set_trace()

def harmonic_mean(var):
    import pdb; pdb.set_trace()

_mean_method = {
    "arithmetic": arithmetic_mean,
    "geometric": geometric_mean,
    "harmonic": harmonic_mean,
}

class NCMean(pyloco.Task):
    """Read a NCD data file and output a mean value

'ncmean' task reads a NCD data file and output a mean value

Examples
---------
"""
    _name_ = "ncmean"
    _version_ = "0.1.0"

    def __init__(self, parent):

        self.add_data_argument("data", required=True, help="NCD data")

        self.add_option_argument("-v", "--variable", nargs="+",
                help="namepath to a variable in a NCD data")

        self.add_option_argument("-m", "--mean", default="arithmetic",
                help="mean type (default=arithmetic)")

        self.register_forward("data", help="mean value")

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
