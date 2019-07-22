# -*- coding: utf-8 -*-
  
def traverse(group, indata, outdata, parent_group=None,
             F1=None, F2=None, F3=None, F4=None):

    if F1: F1(group, indata, outdata, parent_group)

    for g in group["groups"].items():
        d = F2(g, indata, outdata, group) if F2 else outdata
        traverse(g, indata, d, parent_group=group)
        if F3: F3(g, indata, d, group)

    if F4: F4(group, indata, outdata, parent_group)


def get_var(group, name):

    def _get_variables(group, varpaths, outdata, parent_group):

        if varpaths:
            for vname, var in group["vars"].items():
                vpath = group["path"] + vname
                if vpath in varpaths:
                    outdata[vpath] = var

    outvar = normpath(name)
    indata, outdata = [outvar], {}
    traverse(group, indata, outdata, F1=_get_variables)
    return outdata[outvar]


def get_dim(group, name):

    def _get_dimension(group, dimpaths, outdata, parent_group):

        if dimpaths:
            for vname, var in group["dims"].items():
                vpath = group["path"] + vname
                if vpath in dimpaths:
                    outdata[vpath] = var

    outdim = normpath(name)
    indata, outdata = [outdim], {}
    traverse(group, indata, outdata, F1=_get_dimension)
    return outdata[outdim]


class ProxyBase(object):

    def __new__(cls, data):

        obj = super(ProxyBase, cls).__new__(cls)
        obj._data = data
        obj._cnt = 0
        return obj

    def __getattr__(self, attr):

        if attr in self._data:
            return self._data[attr]

        raise AttributeError("'%s' object has no attribute '%s'" %
                             (self.__class__.__name__, attr))


class VarProxy(ProxyBase):

    def __getitem__(self, key):

        if key == slice(None, None, None):
            return self._data["data"]

        else:
            return self._data["data"][key]

    def __setitem__(self, key, value):

        if key == slice(None, None, None):
            self._data["data"] = value

        else:
            raise Exception("Unsupported slicing")


class DimProxy(ProxyBase):

    def __getitem__(self, key):

        if key == slice(None, None, None):
            return self._data["variable"]["data"]

        else:
            return self._data["variable"]["data"][key]

    def __setitem__(self, key, value):

        if key == slice(None, None, None):
            self._data["variable"]["data"] = value

        else:
            raise Exception("Unsupported slicing")


class GroupProxy(ProxyBase):

    def __getattr__(self, attr):

        if attr in self._data["vars"]:
            return VarProxy(self._data["vars"][attr])

        elif attr in self._data["dims"]:
            return DimProxy(self._data["dims"][attr])

        elif attr in self._data and attr not in ("vars", "dims", "groups"):
            return self._data[attr]

        elif attr in self._data["groups"]:
            return GroupProxy(self._data["groups"][attr])

        else:
            raise AttributeError("'GroupProxy' object has no attribute '%s'" % attr)
