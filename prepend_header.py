'''
This program is a command-line tool that allows users to add copyright and legal notices
to source files in software repositories
Command line usage: prepend_header FILE DIR [options]
'''

#!/usr/bin/env python

import argparse
import glob2
import logging
import os
import re

def main():
  verbosity_setup()
  parse()

def parse():
  parser = argparse.ArgumentParser(description = 'Append to files in directories')
  parser.add_argument('FILE', type = str, 
                  help = 'the header to be prepend to each source file (a plain-text file).')
  parser.add_argument('DIR', type = str, 
                  help = 'the path to the directory that contains the files to which the header will be prepended.')
  parser.add_argument('--add', action = 'append', 
                  help = 'add files matching the specified glob (prefixed with the base directory) to the processing queue')
  parser.add_argument('--rm', action = 'append', 
                  help = 'remove files matching the specified glob (prefixed with the base directory) from the processing queue')
  parser.add_argument('--path', type = str, 
                  help = 'replacing template path with actual project path')
  parser.add_argument('--verbose', action = 'store_true', 
                  help = 'raise the verbosity level (log debug and information messages to the standard error stream)')
  parser.add_argument('--version', action = 'version', version = '%(prog)s version 1.0', 
                  help = 'display the version')
  args = parser.parse_args()

  assert os.path.exists(args.FILE), 'File path is incorrect! Could not find the text file at ' + args.FILE
  assert os.path.isdir(args.DIR), 'Directory path is incorrect!'
  if (not args.add):
    logging.error('--add field is required')
  elif (args.add):
    acc = process_files(args.DIR, args.add, args.rm)
    execute(args.FILE, args.DIR, acc, args.verbose, args)
    identify_project_paths(args.DIR, acc, args.path)
    return 0

def identify_project_paths(directory, acc_list, path):
  files = {}
  for i in acc_list:
    files[i] = i.lstrip(directory)
  if (os.name == 'nt'): #check if running on Windows environment
    files = convert_paths(files)
  append_paths_to_files(files, path)

def append_paths_to_files(files, path):
  for key, value in files.items():
    s = open(key).read()
    s = s.replace(str(path), value)
    f = open(key, 'w')
    f.write(s)
    f.close()

def convert_paths(files):
  for key, value in files.items():
    x = re.sub('\\\\', '/', value)
    files[key] = x
  return files

def process_files(directory, include_files, exclude_files):
  include_list = include(directory, include_files)
  if (not exclude_files):
    exclude_list = []
  else:
    exclude_list = exclude(directory, exclude_files)
  acc = join(include_list, exclude_list)
  return acc

def execute(textfile, directory, acc, verbosity, cmd):
  if (verbosity):
    log(textfile, cmd, acc, verbosity)
  else:
    insert_headers(textfile, acc, verbosity)

def verbosity_setup():
  logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def log(textfile, cmd, acc, verbosity):
  logging.info('Command-line Input:' + str(cmd))
  logging.debug('Identified ' + str(len(acc)) + ' files')
  list_files(acc)
  input('Press Enter to continue')
  logging.info('Prepending headers:')
  insert_headers(textfile, acc, verbosity)

def list_files(list):
  for filename in list:
    print (filename)

def include(directory, include_files):
  include_list = []
  for i in include_files:
    include = str(directory) + i
    for name in glob2.glob(include):
      include_list.append(name)
  return include_list

def exclude(directory, exclude_files):
  exclude_list = []
  for e in exclude_files:
    exclude = str(directory) + e
    for name in glob2.glob(exclude):
      exclude_list.append(name)
  return exclude_list

def join(include, exclude):
  for excludefile in exclude:
    if excludefile in include:
      include.remove(excludefile)
  return include

def insert_headers(textfile, append_list, verbosity):
  with open(textfile, 'r') as original:data1 = original.read()
  for filename in append_list:
    with open(filename, 'r') as modified:data2 = modified.read()
    with open(filename, 'w') as original:data3 = original.write(data1)
    with open(filename, 'a') as original:data3 = original.write(data2)
    if (verbosity):
      print(filename)

if __name__ == '__main__':
  main()
