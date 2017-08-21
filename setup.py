#!/usr/bin/env python

from distutils.core import setup

setup(
  name = 'python-licensing-library',
  version = '1.0',
  description = 'Prepend headers to selected source files.',
  license = 'ECL-2.0',
  author = 'Van A. Nguyen',
  author_email = 'van.a.nguyen@pnnl.gov',
  packages = ['python-licensing-library'],
  long_description = open('README.md').read(),
  package_data = {'': ['requirements.txt']},
  data_files = [('', ['LICENSE', 'NOTICE', 'WARRANTY'])],
  include_package_data = True,
  install_requires = [
    'glob2==0.5',
  ],
  classifiers = [
    'License :: ECL-2.0',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries',
  ],
)
