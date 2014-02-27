#!/usr/bin/env python

from distutils.core import setup
from os.path import abspath, dirname, join
import re

NAME = 'robotremoteserver'
CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
""".strip().splitlines()
CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, 'src', NAME+'.py')) as source:
    VERSION = re.search("\n__version__ = '(.*)'\n", source.read()).group(1)
with open(join(CURDIR, 'README.rst')) as readme:
    README = readme.read()

setup(
    name             = NAME,
    version          = VERSION,
    author           = 'Robot Framework Developers',
    author_email     = 'robotframework@gmail.com',
    url              = 'https://github.com/robotframework/PythonRemoteServer',
    download_url     = 'https://pypi.python.org/pypi/robotremoteserver',
    license          = 'Apache License 2.0',
    description      = 'Python Remote Server for Robot Framework',
    long_description = README,
    keywords         = 'robotframework testing testautomation remote',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    package_dir      = {'': 'src'},
    py_modules       = [NAME],
)
