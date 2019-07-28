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

    def pre_perform(self, targs):

        if isinstance(targs.data, str):
            retval, forward = pyloco.perform("ncread", argv=[targs.data, "-q"])
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
