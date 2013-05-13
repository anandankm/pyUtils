#! /usr/bin/python2.7

__author__="Anandan Rangasmay <andy.compeer@gmail.com>"
__date__ ="$Apr 25, 2013"

import time, datetime
import threading, linecache


class readThread(object):
    def __init__(self, f):
        self.ifile = f
        self.thdsperfile = 4
        self.totlines = file_utils.nlines(self.ifile)
        self.thds = []
        self.sharedResource = {}

    def getSharedResource(self):
        return self.sharedResource

    class fileThread(threading.Thread):
        def __init__(self, name, fname, start, nlines, shared):
            threading.Thread.__init__(self)
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


    def startThreads(self):
        threadname = "Thread-"
        start = 1
        nlines = self.totlines/self.thdsperfile
        rem = self.totlines%self.thdsperfile
        k = 1
        while k <= self.thdsperfile:
            thrdname = threadname + str(k)
            start += nlines
            if k == self.thdsperfile:
                nlines += rem
            ft = fileThread(thrdname, self.ifile, start, nlines, sharedResource)
            ft.start()
            self.thds.append(ft)
            k += 1

    def joinThreads(self):
        for thd in self.thds:
            thd.join()
            print thd.name, "completed."
