#! /usr/bin/python

__author__="Anandan Rangasmay <andy.compeer@gmail.com>"
__date__ ="$Apr 25, 2013"

import sys

def sentence_itr(file_handle):
    words = []
    for l in file_handle:
        words = l.strip().split()
        if len(words) > 0:
            yield words

def get_file(filename, mode='r'):
    try:
        file_handle = open(filename, mode)
    except IOError as e:
        sys.stderr.write("ERROR: Cannot read input test file: %s.\nError msg: %s.\n" % (filename, e.strerror))
        raise
    return file_handle

def write_output(array, filename):
    file_h = get_file(filename, "w")
    for item in array:
        file_h.write(item + "\n")
