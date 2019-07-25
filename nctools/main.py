import pyloco

class NcTools(pyloco.Manager):
    _name_ = "nctools"
    _version_ = "0.1.5"
    _description_ = "Composable netCDF utilities for data manipulation and plotting"
    _long_description_ = """nctools : Composable netCDF utilities for data manipulation and plotting

**nctools** is a collection of composable Python tools for netCDF data manipulation and plotting.
"""
    _author_='Youngsung Kim',
    _author_email_ ='youngsun@ucar.edu',
    _license_ ='MIT',
    _url_='https://github.com/NCAR/nctools',
 
def main(argv=None):
    return pyloco.main.main(argv=argv, manager=NcTools)
