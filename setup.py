# Python-Licensing-Library: setup.py
# Copyright (c) 2017 Pacific Northwest National Laboratory.
# See LICENSE for details.

#!/usr/bin/env python

from distutils.core import setup

setup(
  name = 'python-licensing-library',
  version = '1.0',
  description = 'Prepend headers to source files',
  license = 'Pacific Northwest National Laboratory',
  author = 'Van Nguyen',
  author_email = 'van.a.nguyen@pnnl.gov',
  packages = ['python-licensing-library'],
  long_description = open('README.txt').read(),
  package_data = {'':['requirements.txt']},
  data_files = [('', ['LICENSE.txt'])],
  include_package_data = True,
  install_requires = [
      'glob2==0.5',
  ], 
  classifiers = [
      'Intended Audience :: PNNL Software Developers',
      'Programming Language :: Python ::3',
      'Topic :: Software Development :: Libraries',
      'License :: Educational Community License 2.0: Pacific Northwest National Laboratory'
  ]
)
