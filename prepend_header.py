'''
This program is a command-line tool that allows users to add copyright and legal notices
to source files in software repositories
Command line usage: prepend_header FILE DIR [options]
'''

#!/usr/bin/python

import argparse
import glob2
import os

def main():
  parse()

def parse():
  parser = argparse.ArgumentParser(description='Append to files in directories')
  parser.add_argument('FILE', type = str, 
                  help='the header to be prepend to each source file (a plain-text file).')
  parser.add_argument('DIR', type = str,
                  help='the path to the directory that contains the files to which the header will be prepended.')
  parser.add_argument('--add', action="append",
                  help='add files matching the specified glob (prefixed with the base directory) to the processing queue')
  parser.add_argument('--rm', action="append",
                  help= 'remove files matching the specified glob (prefixed with the base directory) from the processing queue')
  parser.add_argument('--verbose',
                  help = "raise the verbosity level (log debug and information messages to the standard error stream)")
  args = parser.parse_args()

  assert os.path.exists(args.FILE), "File path is incorrect! Couldn't find the text file at " + args.FILE
  assert os.path.isdir(args.DIR), 'Directory path is incorrect!'
  if (not args.add):
    print ("Please add a directory to include")
    error()
    
  include_list = include(args.FILE, args.DIR, args.add, args.rm)
  if (not args.rm):
    exclude_list = []
  else:
    exclude_list = exclude(args.FILE, args.DIR, args.add, args.rm)
  acc = join(include_list, exclude_list)
  insert_headers(args.FILE, acc)

def include(textfile, directory, include_files, exclude_files):
  include_list = []
  for item in include_files:
    for name in glob2.glob(item):
      include_list.append(name)
  return include_list

def exclude(textfile, directory, include_files, exclude_files):
  exclude_list = []
  for item in exclude_files:
    for name in glob2.glob(item):
      exclude_list.append(name)
  return exclude_list

def join(include, exclude):
  for excludefile in exclude:
    if excludefile in include:
      include.remove(excludefile)
  return include

'''More optimized solution to add headers to file'''

def insert_headers(textfile, append_list):
  with open(textfile, 'r') as original:data1 = original.read()
  for filename in append_list:
    with open(filename, 'r') as modified:data2 = modified.read()
    with open(filename, 'w') as original:data = original.write(data1 + data2)

'''Append headers by first copying header to a temp tile, copy the content 
of the file that header is being appended to'''

def add_headers(textfile, directory, include_files, exclude_files):
  with open(textfile) as f:
    for filename in include_files:
      with open("temp.tmp", "w") as f1:
        for line in f:
          f1.write(line)
        f.close()
        f1.write("\n\n") 
        with open("test.txt") as f2:
          for line in f2:
           f1.write(line)
          f1.close()
        f2.close()

def error():
  return 0

if __name__ == "__main__":
  main()
