#! /usr/bin/python2.7

__author__="Anandan Rangasmay <andy.compeer@gmail.com>"
__date__ ="$Apr 25, 2013"

import time, datetime
import threading, linecache

class fileThread(threading.Thread):
    def __init__(self, name, fname, start, nlines, shared):
        self.name = name
        self.fname = fname
        self.start = start
        self.nlines = nlines
        self.shared = shared
        self.counter = 0

    def getnext(self):
        line = linecache.getline(self.fname, self.counter + self.start)
        if line:
            words = line.strip().split()
            shared[words[0]] = words
            self.counter += 1

    def run(self):
        while self.counter < self.nlines:
            self.getnext()


class readThread(object):
    def __init__(self, f):
        self.ifile = f
        self.thdsperfile = 4

    def startThread(self):
        self.totlines = file_utils.nlines(self.ifile)
