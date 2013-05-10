#! /usr/bin/python2.7

__author__="Anandan Rangasmay <andy.compeer@gmail.com>"
__date__ ="$May 9, 2013"

"""
  Add a list of string numerical values
  @lis - the list to be summed up
  @sv - the starting value reduces seeds in with 
"""
def addlist(lis, sv):
    def addfn(x,y): return int(x) + int(y)
    return reduce(addfn, lis, sv)

"""
  Given a dictionary with values as list type or other primitive
  type, yield a tab separated line
"""
def dictlineitr(dic):
    for k, v in dic.iteritems():
        line = str(k) + "\t"
        if isinstance(v, list):
            line += "\t".join(str(x) for x in v)
        else:
            line += str(v)
        yield line
