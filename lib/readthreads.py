#! /usr/bin/python2.7

__author__="Anandan Rangasmay <andy.compeer@gmail.com>"
__date__ ="$Apr 25, 2013"

import time, datetime
import threading, linecache
import file_utils


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
        def __init__(self, name, fname, s, n, shared):
            threading.Thread.__init__(self)
            self.name = name
            self.fname = fname
            self.s = s
            self.nlines = n
            self.shared = shared
            self.counter = 0

        def getnext(self):
            line = linecache.getline(self.fname, self.counter + self.s)
            if line:
                words = line.strip().split()
                self.shared[words[0]] = words
                self.counter += 1

        def run(self):
            while self.counter < self.nlines:
                self.getnext()


    def startThreads(self):
        threadname = "Thread-"
        s = 1
        n = self.totlines/self.thdsperfile
        rem = self.totlines%self.thdsperfile
        k = 1
        while k <= self.thdsperfile:
            thrdname = threadname + str(k)
            if k == self.thdsperfile:
                n += rem
            thread = self.fileThread(thrdname, self.ifile, s, n, self.sharedResource)
            print thread, isinstance(thread, threading.Thread)
            self.thds.append(thread)
            thread.start()
            s += n
            k += 1

    def joinThreads(self):
        for thd in self.thds:
            thd.join()
            print thd.name, "completed."
