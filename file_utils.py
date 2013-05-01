#! /usr/bin/python

__author__="Anandan Rangasmay <andy.compeer@gmail.com>"
__date__ ="$Apr 25, 2013"

import sys, json, gzip

def sentence_itr(file_handle):
    words = []
    for l in file_handle:
        words = l.strip().split()
        if len(words) > 0:
            yield words

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

def write_output(array, filename):
    file_h = get_file(filename, "w")
    for item in array:
        file_h.write(item + "\n")
    file_h.close()

def write_itr(itr, file_handle):
    for line in itr:
        file_handle.write(line)
    file_handle.close()
