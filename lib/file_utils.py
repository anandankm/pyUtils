#! /usr/bin/python2.7

__author__="Anandan Rangasmay <andy.compeer@gmail.com>"
__date__ ="$Apr 25, 2013"

import os, sys, json, gzip, list_utils
from subprocess import Popen,PIPE
import shlex

def nlines(filename):
    p1 = Popen(["wc", "-l", filename], stdout=PIPE)
    return int(p1.communicate()[0].strip().split()[0])

def col_sum(filename, ncol):
    command = "awk -F'\t' '{s+=$" + str(ncol) + "}END{print s}' " + filename
    command = shlex.split(command)
    p1 = Popen(command, stdout=PIPE)
    return int(p1.communicate()[0].strip().split()[0])

def sentence_itr(file_handle):
    words = []
    for l in file_handle:
        words = l.strip().split()
        if len(words) > 0:
            yield words

def get_next(file_handle):
    if file_handle.closed:
        return []
    line = file_handle.readline()
    if line:
        return line.strip().split()
    else:
        file_handle.close()
        return []

""" Defaults to binary read """
def get_gzip(filename, mode='rb'):
    try:
        file_handle = gzip.open(filename, mode)
    except IOError as e:
        sys.stderr.write("ERROR: Cannot read input test file: %s.\nError msg: %s.\n" % (filename, e.strerror))
        raise
    return file_handle

def get_file(filename, mode='r'):
    try:
        file_handle = open(filename, mode)
    except IOError as e:
        sys.stderr.write("ERROR: Cannot read input test file: %s.\nError msg: %s.\n" % (filename, e.strerror))
        raise
    return file_handle

""" Compress some big content (string obj) into a gzip file """
def write_gzip(big_content, filename):
    file_h = get_gzip(filename, "wb")
    file_h.write(big_content)
    file_h.close()

""" Write an obj (better to be a list or a dict) represented as json string to a gzip file """
def write_json_gzip(obj, filename):
    write_gzip(json.dumps(obj), filename)

"""
  Write an array tab separated and keep the file_handle open
  for tail -f.
  Caller needs to take care of closing the file_handle
"""
def tailwrite(arr, file_handle):
    if isinstance(arr,list):
        file_handle.write("\t".join(str(x) for x in arr))
    else:
        file_handle.write(str(arr))
    file_handle.write("\n")
    file_handle.flush()
    os.fsync(file_handle.fileno())

"""
  Write a list of lists to a file tab separated.
"""
def write_arrarr(arrarr, filename):
    file_h = get_file(filename, "w")
    for arr in arrarr:
        file_h.write("\t".join(str(x) for x in arr) + "\n")
    file_h.close()


def write_output(array, filename):
    file_h = get_file(filename, "w")
    for item in array:
        file_h.write(item + "\n")
    file_h.close()

def write_dict(dic, filename):
    file_h = get_file(filename, "w")
    for line in list_utils.dictlineitr(dic):
        file_h.write(line + "\n")
    file_h.close()


def write_itr(itr, file_handle):
    for line in itr:
        file_handle.write(line)
    file_handle.close()
