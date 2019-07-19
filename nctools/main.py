import pyloco

class NcTools(pyloco.Manager):
    _name_ = "nctools"
    _version_ = "0.1.0"

def main():
    pyloco.main.main(manager=NcTools)
