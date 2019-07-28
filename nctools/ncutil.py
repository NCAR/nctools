# -*- coding: utf-8 -*-

import os
import numpy
import pyloco

MAXWIDTH = 50

def _truncate(name, obj):

    text = str(obj)

    if len(text) > MAXWIDTH:
        outtext =(name, "%s..."%text[:MAXWIDTH])

    else:
        outtext = (name, text)

    return outtext


def _pack(lines):

    packed = []
    maxprefix = 0

    for prefix, text in lines:
        maxprefix = max(len(prefix), maxprefix)

    for prefix, text in lines:
        if prefix:
            packed.append(prefix+" "*(maxprefix-len(prefix)+1)+text)

        else:
            packed.append(text)

    return "\n".join(packed)


#def _split(namepath):
#
#    split1 = namepath.split(".", 1)
#    split2 = split1[0].split("[", 1)
#
#    remained = ("["+split2[1]) if len(split2)==2 else ""
#    remained = remained + split1[1] if len(split1)==2 else remained
#
#    return split2[0].strip(), remained


def traverse(group, indata, outdata, parent_group=None,
             F1=None, F2=None, F3=None, F4=None):

    if F1: F1(group, indata, outdata, parent_group)

    for g in group["groups"].items():
        d = F2(g, indata, outdata, group) if F2 else outdata
        traverse(g, indata, d, parent_group=group)
        if F3: F3(g, indata, d, group)

    if F4: F4(group, indata, outdata, parent_group)


#def get_var(group, name):
#
#    def _get_variables(group, varpaths, outdata, parent_group):
#
#        if varpaths:
#            for vname, var in group["vars"].items():
#                vpath = group["path"] + vname
#                if vpath in varpaths:
#                    outdata[vpath] = var
#
#    outvar = normpath(name)
#    indata, outdata = [outvar], {}
#    traverse(group, indata, outdata, F1=_get_variables)
#    return outdata[outvar]
#
#
#def get_dim(group, name):
#
#    def _get_dimension(group, dimpaths, outdata, parent_group):
#
#        if dimpaths:
#            for vname, var in group["dims"].items():
#                vpath = group["path"] + vname
#                if vpath in dimpaths:
#                    outdata[vpath] = var
#
#    outdim = normpath(name)
#    indata, outdata = [outdim], {}
#    traverse(group, indata, outdata, F1=_get_dimension)
#    return outdata[outdim]

def desc_group(group, indata, outdata, parent_group):


    dimnames = list(group["dims"].keys())
    gpath = group["path"]
    lines = []

    lines.append(("", "\n***** variables in group '%s' *****" % gpath))

    for varname in group["vars"].keys():
        if varname in dimnames:
            continue

        if "only" not in indata or gpath+varname in indata["only"]:
            var = group["vars"][varname]
            dims = ["%s:%d"%d for d in zip(var["dimensions"], var["data"].shape)]
            lines.append((varname, "(%s) %s" % (", ".join(dims), str(var["data"].dtype))))

            if "verbose" in indata and indata["verbose"]:
                for n, a in var.items():
                    if not n.startswith("_") and n not in ("data",):
                        lines.append(("   - %s: " % n, str(a)))
                lines.append(("", ""))

    if "verbose" in indata and indata["verbose"]:
        lines.append(("", "\n***** dimensions in group '%s' *****" % gpath))
        for dimname, dimobj in group["dims"].items():
            lines.append((dimname, "name=%s, size=%d, isunlimited=%s" %
                (dimname, dimobj["size"], str(dimobj["isunlimited"]))))
        lines.append(("", ""))

    if "only" not in indata:
        lines.append(("", "\n***** attributes in group '%s' *****" % gpath))

        for attrname, attrobj in group.items():
            if attrname.startswith("_") or attrname in ("vars", "dims", "groups"):
                continue

            if attrname == "ncattrs":
                for ncattrname, ncattrobj in attrobj.items():
                    lines.append(_truncate(ncattrname, ncattrobj))

            else:
                lines.append(_truncate(attrname, attrobj))

    print(_pack(lines))

#def desc_path(group, outdata, parent_group):
#    print("\n[%s]" % group["path"])

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

    def get_rawdata(self):
        return self._data

#    def dump(self, namepath):
#
#        namepath = namepath.strip()
#
#        if namepath:
#            name, remained = _split(namepath)
#            obj = getattr(self, name, None)
#
#            if obj is None:
#                attrs = [a for a in self._data.keys()]
#                print("ERROR: could not find any item specified by '%s'.\n"
#                      "Possible attributes are: %s" % (name, ", ".join(attrs)))
#
#            elif isinstance(obj, ProxyBase):
#                obj = obj.dump(remained)
#
#            elif isinstance(obj, (numpy.ndarray, numpy.generic)):
#                if remained:
#                    if not remained.startswith("["):
#                        remained = "." + remained
#
#                obj = eval("obj"+remained, None, {"obj": obj})
#
#            elif isinstance(obj, dict):
#                if remained.startswith("["):
#                    obj = eval("obj"+remained, None, {"obj": obj})
#
#                elif remained:
#                    n, r = _split(remained)
#
#                    if n and r:
#                        obj = eval("obj['%s']%s" % (n, r), None, {"obj": obj})
#
#                    elif n:
#                        obj = eval("obj['%s']" % n, None, {"obj": obj})
#
#                    elif r:
#                        obj = eval("obj%s" % r, None, {"obj": obj})
#
#            return obj
#
#        else:
#            return self


class VarProxy(ProxyBase):

#    def __getitem__(self, key):
#
#        if key == slice(None, None, None):
#            return self._data["data"]
#
#        else:
#            return self._data["data"][key]
#
#    def __setitem__(self, key, value):
#
#        if key == slice(None, None, None):
#            self._data["data"] = value
#
#        else:
#            raise Exception("Unsupported slicing")

    def __getitem__(self, key):

        return self._data["data"][key]

    def __setitem__(self, key, value):

        self._data["data"][key] = value

    def __str__(self):

        lines = []

        lines.append(_truncate("", "\n**** variable attributes ****"))

        for attr, value in self._data.items():
            if attr == "data":
                continue

            lines.append(_truncate(attr, str(value)))

        lines.append(_truncate("", "\n**** variable data ****\n"))
        packed = _pack(lines)

        return packed + str(self._data["data"])

#    def dump(self, namepath):
#
#        if namepath.startswith("["):
#            return eval("obj"+namepath, None, {"obj": self.data})
#
#        else:
#            return super(VarProxy, self).dump(namepath)

class DimProxy(ProxyBase):

#    def __getitem__(self, key):
#
#        if key == slice(None, None, None):
#            return self._data["variable"]["data"]
#
#        else:
#            return self._data["variable"]["data"][key]
#
#    def __setitem__(self, key, value):
#
#        if key == slice(None, None, None):
#            self._data["variable"]["data"] = value
#
#        else:
#            raise Exception("Unsupported slicing")

    def __getitem__(self, key):

        return self._data["variable"]["data"][key]

    def __setitem__(self, key, value):

        self._data["variable"]["data"][key] = value

    def __str__(self):

        lines = []

        lines.append(_truncate("", "\n**** dimension attributes ****"))

        for attr, value in self._data.items():
            if attr == "variable":
                continue

            lines.append(_truncate(attr, str(value)))

        packed = _pack(lines)

        varobj = VarProxy(self._data["variable"])

        return packed + "\n" + str(varobj)

#    def dump(self, namepath):
#
#        if namepath.startswith("["):
#            variable = VarProxy(self.variable)
#            return variable.dump(namepath)
#
#        else:
#            return super(DimProxy, self).dump(namepath)

class GroupProxy(ProxyBase):

    def __getattr__(self, attr):

        if attr in self._data["vars"]:
            return VarProxy(self._data["vars"][attr])

        elif attr in self._data["dims"]:
            return DimProxy(self._data["dims"][attr])

        elif attr in self._data and attr not in ("vars", "dims", "groups"):
            return self._data[attr]

        elif "ncattrs" in self._data and attr in self._data["ncattrs"]:
            return self._data["ncattrs"][attr]

        elif attr in self._data["groups"]:
            return GroupProxy(self._data["groups"][attr])

        else:
            raise AttributeError("'GroupProxy' object has no attribute '%s'" % attr)

    def __str__(self):

        lines = []

        lines.append(_truncate("", "\n**** group attributes ****"))

        for attr, value in self._data.items():
            if attr in ("vars", "dims", "groups"):
                continue

            if attr == "ncattrs":
                for _n, _v in self._data["ncattrs"].items():
                    lines.append(_truncate(_n, str(_v)))
            else:
                lines.append(_truncate(attr, str(value)))

        packed = _pack(lines)
        varlines = []
        dimlines = []
        grouplines = []

        for vname, vobj in self._data["vars"].items():
            varlines.append(str(VarProxy(vobj)))

        for dname, dobj in self._data["dims"].items():
            dimlines.append(str(DimProxy(dobj)))

        for gname, gobj in self._data["groups"].items():
            grouplines.append(str(GroupProxy(gobj)))

        return (packed + "\n" + "\n".join(varlines) + "\n".join(dimlines) +
                "\n".join(grouplines))

def ncdproxy(ncd):

    env = {}

    for k, g in ncd["groups"].items():
        env[k] = GroupProxy(g)

    for k, a in ncd.items():
        if k not in ("vars", "dims", "groups"):
            if k == "ncattrs":
                for x, y in a.items():
                    env[x] = y
            else:
                env[k] = a

    for k, d in ncd["dims"].items():
        env[k] = DimProxy(d)

    for k, v in ncd["vars"].items():
        env[k] = VarProxy(v)

    return env
