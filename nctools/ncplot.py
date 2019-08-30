# -*- coding: utf-8 -*-

import os
import pyloco
from nctools.ncutil import (GroupProxy, DimProxy, VarProxy, ncdproxy)


class NCPlot(pyloco.taskclass("matplot")):
    """Read a NCD data and generate plot(s)

'ncplot' task reads a NCD data and generates plots.

Examples
---------
"""
    _name_ = "ncplot"
    _version_ = "0.1.3"
    _install_requires = ["matplot"]

    def __init__(self, parent):

        super(NCPlot, self).__init__(parent)

        self.set_data_argument("data", required=True,
                help="data input in NetCDF-dictionary format")

        self.add_option_argument("-v", "--variable", action="append", help="variable name")

    def pre_perform(self, targs):

        if isinstance(targs.data, str):
#            pathsplit = targs.data.split(":", 1)
#            if len(pathsplit) == 2:
#                filepath, varpath = pathsplit
#
#            else:
#                filepath, varpath = pathsplit[0], None

            if not os.path.isfile(targs.data):
                raise Exception("'%s' is not correct file path." % targs.data)

            argv = [targs.data]

            if targs.variable:
                for var in targs.variable:
                    argv.extend(["-v", var])

            retval, forward = pyloco.perform("ncread", argv=argv)
            targs.data = forward["data"] 

        proxies = ncdproxy(targs.data)
        self._env.update(proxies)

        super(NCPlot, self).pre_perform(targs)
#    
#    @staticmethod
#    def plot_contourf(plotter, opt, targs):
#
#        return NCPlot.plot_contour(plotter, opt, targs, fill=True)
#
#    @staticmethod
#    def plot_contour(plotter, opt, targs, fill=False):
#
#        plotfunc = "contourf" if fill else "contour"
#        opt.context[0] = plotfunc
#        targs.plot.append(opt)
