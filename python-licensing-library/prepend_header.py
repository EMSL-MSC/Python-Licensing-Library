#!/usr/bin/env python

# Python-Licensing-Library: python-licensing-library/prepend_header.py
#
# Copyright (c) 2017 Pacific Northwest National Laboratory (see the file NOTICE).
#
# This material is released under the ECL-2.0 license (see the file LICENSE).
#
# This material is released under warranty (see the file WARRANTY).

import argparse
import glob2
import logging
import os
import re

def main():
  """
  Main function.

  """
  verbosity_setup()
  parse()

def parse():
  """
  Method to process input and parse command-line arguments.

  Args:
      FILE (str): the header to be prepend to each source file (a plain-text file).
      DIR (str): the base directory for the software repository.
      --add = GLOB: path name (can contain shell-style wildcards) containing files to be added to the processing queue.
      --rm = GLOB: path name (can contain shell-style wildcards) containing files to be removed from the processing queue.
      --path (str): template path.
      --verbose (str): option to raise verbosity level (log debug and information messages to the standard error stream).
      --version (str): display the version of library.
      --help: display the help message.

  Returns:
      returns 0 if no error found.

  """
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
                  help = 'replace template path with actual project path')
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
    if (args.path):
      identify_project_paths(args.DIR, acc, args.path)
    return 0

def identify_project_paths(directory, acc_list, path):
  """
  Identifies names of project files without the base path. This method is only executed when --path=str is included in args.

  Args:
      directory: the base directory.
      acc_list: list of files with template paths.
      path=str: template path (e.g., 'path/to/file.rb').

  Returns:
      returns 0 if no error found.

  """
  files = {}
  for i in acc_list:
    files[i] = i.lstrip(directory)
  if (os.name == 'nt'): #check if running on Windows environment
    files = convert_paths(files)
  append_paths_to_files(files, path)

def append_paths_to_files(files, path):
  """
  Replaces template path with project path in selected source files. This method is only executed when --path=str is included in args.

  Args:
      files: dictionary containing directories (keys) and (UNIX-style) project paths (values).
      path=str: template path (e.g., 'path/to/file.rb').

  Returns:
      Template paths are replaced with project paths.

  """
  for key, value in files.items():
    s = open(key).read()
    s = s.replace(str(path), value)
    f = open(key, 'w', newline='\n')
    f.write(s)
    f.close()

def convert_paths(files):
  """
  Converts '\' character in Windows paths to '/'. This method is only executed when script is running on Windows environment.

  Args:
      files: a dictionary containing full paths and their project paths (in Windows style).

  Returns:
      files: a dictionary containing full paths and their project paths (in UNIX style).

  """
  for key, value in files.items():
    x = re.sub('\\\\', '/', value)
    files[key] = x
  return files

def process_files(directory, include_files, exclude_files):
  """
  Compiles an accumulator containing all files to which the header will be prepended.

  Args:
      directory (str): the base directory.
      include_files (str): path name containing files to be added to the processing queue.
      exclude_files (str): path name containing files to be removed from the processing queue.

  Returns:
      acc: a list/accumulator with all files to which the header will be prepended.

  """
  include_list = include(directory, include_files)
  if (not exclude_files):
    exclude_list = []
  else:
    exclude_list = exclude(directory, exclude_files)
  acc = join(include_list, exclude_list)
  return acc

def execute(textfile, directory, acc, verbosity, cmd):
  """
  Prepends headers to selected files. If --verbose is specified, then debug information will be logged in standard error stream. 

  Args:
      textfile (str): directory containing header to be prepended.
      directory (str): the base directory.
      acc: a list/accumulator with all files to which the header will be prepended.
      verbosity (bool): value indicate whether user chooses to have information logged to standard error stream.
      cmd (str): command-line input.

  Returns:
      acc: a list/accumulator with all files to which the header will be prepended.

  """
  if (verbosity):
    log(textfile, cmd, acc, verbosity)
  else:
    insert_headers(textfile, acc, verbosity)

def verbosity_setup():
  """
  Sets up verbosity message template.

  """
  logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def log(textfile, cmd, acc, verbosity):
  """
  Inserts headers to selected files and logs information to standard error stream. This method is executed only when --verbose is indicated in args.

  Args:
      textfile (str): directory containing header to be prepended.
      cmd (str): command-line input.
      acc: a list/accumulator with all files to which the header will be prepended.
      verbosity (bool): value indicate whether user chooses to have information logged to standard error stream.

  Returns:
      The standard error stream will display command line input, number of files in which header will be added, and the names of those files.

  """
  logging.warning('Command-line Input:' + str(cmd))
  if (len(acc) == 0):
    logging.error('No file is found')
  else:
    logging.info('Identified ' + str(len(acc)) + ' files')
    list_files(acc)
    logging.info('Prepending headers:')
    insert_headers(textfile, acc, verbosity)

def list_files(list):
  """
  List all items in a list.

  Args:
      list: a list containing 0 or more items.

  Returns:
      The standard error stream will display all items from a given list.

  """
  for filename in list:
    print (filename)

def include(directory, include_files):
  """
  Identifies all files mentioned in --add=GLOB and stores the names of those files in a list.

  Args:
      directory (str): the base directory.
      include_files: GLOB containing files to be added to the processing queue.

  Returns:
      include_list: list containing directories of all files matching --add=GLOB.

  """
  include_list = []
  for i in include_files:
    include = str(directory) + i
    for name in glob2.glob(include):
      include_list.append(name)
  return include_list

def exclude(directory, exclude_files):
  """
  Identifies all files mentioned in --rm=GLOB and stores the names of those files in a list.

  Args:
      directory (str): the base directory.
      exclude_files: GLOB containing files to be removed to the processing queue.

  Returns:
      exclude_list: list containing directories of all files matching --rm=GLOB.

  """
  exclude_list = []
  for e in exclude_files:
    exclude = str(directory) + e
    for name in glob2.glob(exclude):
      exclude_list.append(name)
  return exclude_list

def join(include, exclude):
  """
  Removes all items within list of excluded files from list of included files.

  Args:
      include: list containing directories of all files matching --add=GLOB.
      exclude: list containing directories of all files matching --rm=GLOB.

  Returns:
      include: a final list with all files to which the header will be prepended.

  """
  for excludefile in exclude:
    if excludefile in include:
      include.remove(excludefile)
  return include

def insert_headers(textfile, append_list, verbosity):
  """
  Appends headers to selected files and logs debug information if specified

  Args:
      textfile (str): directory containing header to be prepended.
      append_list: a list with all files to which the header will be prepended.
      verbosity (bool): value indicate whether user chooses to have information logged to standard error stream.

  Returns:
      Source files with prepended headers.

  """
   with open(textfile, 'r', newline='\n') as original:data1 = original.read()
   for filename in append_list:
     with open(filename, 'r', newline='\n') as modified:data2 = modified.read()
     with open(filename, 'w', newline='\n') as original:data3 = original.write(data1)
     with open(filename, 'a', newline='\n') as original:data3 = original.write(data2)
     if (verbosity):
      print(filename)

if __name__ == '__main__':
  """
  Performs a main check so that this script can run on its own (rather than being imported from another module).

  """
  main()
