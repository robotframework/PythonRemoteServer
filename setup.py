#!/usr/bin/env python

from distutils.core import setup
from os.path import abspath, dirname, join

# Get __version__ dynamically
execfile(join(dirname(abspath(__file__)), 'src', 'robotremoteserver.py'))

DESCRIPTION = """
Robot Framework remote servers allow hosting test libraries on different
machines and/or interpreters than Robot Framework itself is running on.
This version is implemented with Python and supports also Jython (JVM) and
IronPython (.NET). Separate implementations exist for other languages.
For more information about the remote library interface in general see
http://code.google.com/p/robotframework/wiki/RemoteLibrary
""".strip()
CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
""".strip().splitlines()

setup(
    name         = 'robotremoteserver',
    version      = __version__,
    author       = 'Robot Framework Developers',
    author_email = 'robotframework@gmail.com',
    url          = 'https://github.com/robotframework/PythonRemoteServer',
    license      = 'Apache License 2.0',
    description  = 'Robot Framework remote server',
    long_description = DESCRIPTION,
    keywords     = 'robotframework testing testautomation',
    platforms    = 'any',
    classifiers  = CLASSIFIERS,
    package_dir  = {'': 'src'},
    py_modules   = ['robotremoteserver']
)
