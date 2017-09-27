#!/usr/bin/env python

from os.path import abspath, dirname, join
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


NAME = 'robotremoteserver'
CLASSIFIERS = '''
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: Jython
Programming Language :: Python :: Implementation :: IronPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Software Development :: Testing
Framework :: Robot Framework
'''.strip().splitlines()
CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, 'src', NAME+'.py')) as source:
    VERSION = re.search("\n__version__ = '(.*)'", source.read()).group(1)
with open(join(CURDIR, 'README.rst')) as readme:
    README = readme.read()


setup(
    name             = NAME,
    version          = VERSION,
    author           = u'Pekka Kl\xe4rck and contributors',
    author_email     = 'robotframework@gmail.com',
    url              = 'https://github.com/robotframework/PythonRemoteServer',
    download_url     = 'https://pypi.python.org/pypi/robotremoteserver',
    license          = 'Apache License 2.0',
    description      = 'Robot Framework remote server implemented with Python',
    long_description = README,
    keywords         = 'robotframework testing testautomation remoteinterface',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    package_dir      = {'': 'src'},
    py_modules       = [NAME],
)
