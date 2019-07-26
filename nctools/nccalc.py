# -*- coding: utf-8 -*-

import os 
import numpy
import pyloco

from nctools.ncutil import GroupProxy, DimProxy, VarProxy, ncdproxy

# TODO: create toncdict function that converts data to NCD format
# TODO: output should have NCD format too

class NCCalc(pyloco.Task):
    """Read a NCD data file and output numpy-calculated value

'ncmean' task reads a NCD data file and outputs numpy-calculated value

Examples
---------
"""
    _name_ = "nccalc"
    _version_ = "0.1.1"

    def __init__(self, parent):

        self.add_data_argument("data", required=True, help="NCD data")

        self.add_option_argument("-c", "--calc", action="append",
                param_parse=True, help="(E,P) numpy calculation")
        self.add_option_argument("--np", action="store_true", help="use 'np' as 'numpy' abbreviation")

        self.register_forward("data", help="value")

    def perform(self, targs):

        data = None
        outdata = None

        if isinstance(targs.data, dict):
            data = targs.data

        elif os.path.isfile(targs.data):
            retval, forward = pyloco.perform("ncread", argv=[targs.data])
            data = forward["data"]

        if not isinstance(data, dict):
            raise Exception("Specified input is not correct: %s" % str(targs.data)) 

        self._env["numpy"] = numpy

        if targs.np:
            self._env["np"] = numpy

        proxies = ncdproxy(data)
        self._env.update(proxies)

        evaluated = {}

        if targs.calc:
            for calc in targs.calc:
                for name, expr in calc.kwargs.items():
                    self._env[name] = eval(expr, self._env)
                    evaluated[name] = self._env[name]

        else:
            print("ERROR: No expression is specified by '-e' option")
            sys.exit(-1)

        self.add_forward(data=evaluated)
