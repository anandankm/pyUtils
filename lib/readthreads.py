#! /usr/bin/python2.7

__author__="Anandan Rangasmay <andy.compeer@gmail.com>"
__date__ ="$Apr 25, 2013"

import time, datetime
import threading, linecache
import file_utils
import inspect


class readThread(object):
    def __init__(self, f, shared, nt=4, attr=""):
        self.ifile = f
        self.thdsperfile = nt
        self.totlines = file_utils.nlines(self.ifile)
        self.thds = {}
        self.sharedResource = shared
        self.attr = attr
        self.isrun = 0
        self.checkAttr()
        self.setThreads()

    def checkAttr(self):
        if self.attr:
            """ Some reflection magic """
            self.attr = getattr(self.sharedResource, self.attr)
            if not callable(self.attr):
                self.attr = ""
            else:
                args = inspect.getargspec(self.attr).args
                if 'self' in args:
                    args.remove('self')
                if len(args) != 1:
                    self.attr = ""


    def setThreads(self):
        threadname = "Thread-"
        s = 1
        n = self.totlines/self.thdsperfile
        rem = self.totlines%self.thdsperfile
        k = 1
        while k <= self.thdsperfile:
            thrdname = threadname + str(k)
            if k == self.thdsperfile:
                n += rem
            thread = self.fileThread(thrdname, self.ifile, s, n,\
                    self.sharedResource, self.attr)
            self.thds[thread] = 1
            s += n
            k += 1

    def getSharedResource(self):
        return self.sharedResource

    class fileThread(threading.Thread):
        def __init__(self, name, fname, s, n, shared, methodattr=""):
            threading.Thread.__init__(self)
            self.name = name
            self.fname = fname
            self.s = s
            self.nlines = n
            self.shared = shared
            self.methodattr = methodattr
            self.counter = 0

        def getnext(self):
            lineno = self.counter + self.s
            line = linecache.getline(self.fname, lineno)
            if line:
                words = line.strip().split()
                if self.methodattr:
                   self.methodattr(line)
                else:
                    self.shared[words[0]] = words
                self.counter += 1

        def run(self):
            while self.counter < self.nlines:
                self.getnext()

    def printThreads(self):
        for thd in self.thds.keys():
            print thd.name, thd.s, thd.nlines + thd.s, thd.nlines

    def startThreads(self):
        for thd in self.thds.keys():
            thd.start()
            self.isrun += 1
            print "Started", thd.name

    def joinThreads(self):
        while self.isrun > 0:
            for thd in self.thds.keys():
                if not thd.isAlive():
                    if self.thds[thd] == 1:
                        self.isrun -= 1
                        self.thds[thd] = 0
                else:
                    thd.join(0.25)
        print "All threads completed."
