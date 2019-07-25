# -*- coding: utf-8 -*-

import os
import pyloco

from nctools.ncutil import traverse, desc_group, GroupProxy


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

        self.register_forward("data",
                help="netcdf variables in Python dictionary")

    def perform(self, targs):

        data = None

        if isinstance(targs.data, dict):
            data = targs.data

        elif os.path.isfile(targs.data):
            retval, forward = pyloco.perform("ncread", argv=[targs.data])
            data = forward["data"]

        if not isinstance(data, dict):
            raise Exception("Specified input is not correct: %s" % str(targs.data)) 


        if hasattr(targs, "path") and targs.path:
            group = GroupProxy(data)
            outdata = group.dump(targs.path)

        else:
            attrs = {"verbose": False}
            traverse(data, attrs, {}, F1=desc_group)
            outdata = ""

        if outdata:
            print(outdata)

        self.add_forward(data=outdata)
