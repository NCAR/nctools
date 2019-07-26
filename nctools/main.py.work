import os
import pyloco

here = os.path.abspath(os.path.dirname(__file__))

class NcTools(pyloco.Manager):
    _name_ = "nctools"
    _version_ = "0.1.11"
    _description_ = "Composable netCDF utilities for data manipulation and plotting"
    _long_description_ = """nctools : Composable netCDF utilities for data manipulation and plotting

**nctools** is a collection of composable Python tools for netCDF data manipulation and plotting.
"""
    _author_='Youngsung Kim',
    _author_email_ ='youngsun@ucar.edu',
    _license_ ='MIT',
    _url_='https://github.com/NCAR/nctools',
    _default_tasks_ = {
        "ncread": os.path.join(here, "ncread.py"),
        "ncdump": os.path.join(here, "ncdump.py"),
        "nccalc": os.path.join(here, "nccalc.py"),
        "ncplot": os.path.join(here, "ncplot.py"),
    }
 
def main(argv=None):
    import sys

    if argv is None:
        argv = sys.argv[1:]

    if argv and argv[0] in NcTools._default_tasks_:
        argv[0] = NcTools._default_tasks_[argv[0]]

    return pyloco.main.main(argv=argv, manager=NcTools)

