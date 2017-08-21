# Python-Licensing-Library

Copyright (C) 2017 Pacific Northwest National Laboratory.

## Description

The purpose of this library is to provide software developers to quickly prepend headers to selected source file.
It provides several options to allow flexibility and control over files to which the headers will be prepended.

The library can be used in Microsoft Windows, Linux, and macOS operating systems.

## Usage

`prepend_header.py FILE DIR [options]`

where
* `FILE` = the header to be prepend to each source file (a plain-text file);

* `DIR` = the base directory for the software repository; and,

* `[options]` = the command-line options.

### Command-line Options

* `--help` = Display the help message.

* `--version` = Display the version.

* `--verbose` = Raise the verbosity level (log debug and information messages to the standard error stream).

* `--add=GLOB` = Add files matching the specified glob (prefixed with the base directory) to the processing queue.

* `--rm=GLOB` = Remove files matching the specified glob (prefixed with the base directory) from the processing queue.

* `--path=str` = Replace template path with actual project path.

Before installing the __Python-Licensing-Library__ package, please make sure that you have already installed Python and have an application to unpack a `*.tar.gz` file.

## Installation Instructions

1. Extract the __Python-Licensing-Library__ package.

2. Under the directory containing `setup.py`, execute command `python setup.py install`.

3. Install [glob2](https://pypi.python.org/pypi/glob2). Under the directory containing `requirements.txt`, execute command `pip install -r requirements.txt`.

To verify installation of dependency use `pip list`.

4. The package is ready to be used. For assistance on how to use the tool, execute `python prepend_header.py --help`.
