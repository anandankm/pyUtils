#! /usr/bin/python2.7

__author__="Anandan Rangasmay <andy.compeer@gmail.com>"
__date__ ="$Apr 25, 2013"

import time, datetime
import threading, linecache
import file_utils
import inspect
import random


class readThread(object):
    def __init__(self, f, shared, nt=4, attr="", info=0):
        self.ifile = f
        self.thdsperfile = nt
        self.totlines = file_utils.nlines(self.ifile)
        self.thds = {}
        self.sharedResource = shared
        self.attr = attr
        self.isrun = 0
        self.info = info
        self.infothread = self.threadinfo(self)
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

    class threadinfo(threading.Thread):
        def __init__(self, readT):
            threading.Thread.__init__(self)
            self.thds = readT.thds
            self.readT = readT

        def run(self):
            self.st = time.time()
            perc_r = range(6,100,6)
            len_perc = len(perc_r)
            i = 0
            while self.readT.isrun > 0:
                result_str = ""
                time.sleep(2.0)
                result_cnt = 0
                for thd in self.thds.keys():
                    result_cnt += thd.counter
                    perc = "0%"
                    if thd.counter != 0:
                        perc = str(100*thd.counter/float(thd.nlines)) + "%"
                    result_str += str([thd.name, thd.counter, perc])
                    result_str += ", "
                print result_str

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
                   self.methodattr(words)
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
            time.sleep(random.random()/float(1000))
            thd.start()
            self.isrun += 1
            print "Started", thd.name
        if self.info:
            time.sleep(1.0)
            self.infothread.start()

    def joinThreads(self):
        while self.isrun > 0:
            for thd in self.thds.keys():
                if not thd.isAlive():
                    if self.thds[thd] == 1:
                        self.isrun -= 1
                        self.thds[thd] = 0
                else:
                    thd.join(0.25)
        if self.info:
            print "Waiting for 'threadinfo' thread to join"
            self.infothread.join()
            print "Info thread joined"
