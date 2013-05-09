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
    return reduce(addfn, line, sv)
