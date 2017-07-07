#!/usr/bin/python

import sys
import os
import argparse
import fileinput
import glob
import fnmatch

def main():
  parse()

def parse():
  parser = argparse.ArgumentParser(description='Append to files in directories')
  parser.add_argument('file', type = str, 
                  help='the header to be prepend to each source file (a plain-text file).')
  parser.add_argument('dir', type = str,
                  help='the path to the directory that contains the files to which the header will be prepended.')
  parser.add_argument('--add', action="append",
                  help='add files matching the specified glob (prefixed with the base directory) to the processing queue')
  parser.add_argument('-rm', action="append",
                  help= 'remove files matching the specified glob (prefixed with the base directory) from the processing queue')
  args = parser.parse_args()

  assert os.path.exists(args.file), " File path is incorrect! Couldn't find the text file at " + args.file
  assert os.path.isdir(args.dir), 'Directory path is incorrect!'
  if (not args.add):
    print ("Please add a directory to include")
  if (args.rm):
    assert os.path.exists(args.rm), 'File path in exclude path is incorrect!'
  select_files(args.file, args.dir, args.add, args.rm)

def select_files(textfile, directory, include_files, exclude_files):
  count = 0
  acc = []
  for x in os.walk(directory):
    print x[0]

def add_headers(textfile, directory, include_files, exclude_files):
  with open(textfile) as f:
    for filename in include_files:
      with open("temp.tmp", "w") as f1:
        for line in f:
          f1.write(line)
        f.close()
        f1.write("\n\n") 
        with open("admin.txt") as f2:
          for line in f2:
           f1.write(line)
          f1.close()
        f2.close()

def error():
    print ("-----------------------------------------------------------------------")
    print("Incorrect number of arguments")
    print ("Usage: prepend_header.py FILE DIR [--include=GLOB]* [--exclude=GLOB]*")


main()