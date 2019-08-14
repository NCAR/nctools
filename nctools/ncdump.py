# -*- coding: utf-8 -*-

import os
import pyloco

from nctools.ncutil import traverse, desc_group, ncdproxy


class NCDump(pyloco.Task):
    """Read a NCD data file and output a specified object in the file

'ncdump' task reads a NCD data file and output a specified object in the file.

Examples
---------
"""
    _name_ = "ncdump"
    _version_ = "0.1.0"

    def __init__(self, parent):

        self.add_data_argument("data", required=True, help="NCD data")

        self.add_option_argument("-p", "--path", help="namepath in a NCD data")
        self.add_option_argument("-q", "--quite", action="store_true", help="no output on screen")

        self.register_forward("data",
                help="netcdf variables in Python dictionary")

    def perform(self, targs):

        data = None

        if isinstance(targs.data, dict):
            data = targs.data

        elif os.path.isfile(targs.data):
            retval, forward = pyloco.perform("ncread", argv=[targs.data, "-q"])
            data = forward["data"]

        if not isinstance(data, dict):
            raise Exception("Specified input is not correct: %s" % str(targs.data)) 

        outdata = None

        if hasattr(targs, "path") and targs.path:
            self._env.update(ncdproxy(data))
            outdata = eval(targs.path, self._env)
            data = outdata.get_rawdata() if hasattr(outdata, "get_rawdata") else outdata
            self.add_forward(data=data)

        elif targs.quite:
            self.add_forward(data=None)

        else:
            attrs = {"verbose": False}
            traverse(data, attrs, {}, F1=desc_group)
            self.add_forward(data=None)

        if outdata is not None and not targs.quite:
            print(str(outdata))
