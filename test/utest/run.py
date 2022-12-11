#!/usr/bin/env python

from os.path import abspath, dirname, join
import os
import sys
import unittest


curdir = dirname(abspath(__file__))
sys.path.insert(0, join(curdir, '..', '..', 'src'))
sys.path.insert(0, join(curdir, '..', 'libs'))

test_files = [f[:-3] for f in os.listdir(curdir)
              if f.startswith('test_') and f.endswith('.py')]
suite = unittest.defaultTestLoader.loadTestsFromNames(test_files)
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
rc = len(result.failures) + len(result.errors)
sys.exit(rc)
