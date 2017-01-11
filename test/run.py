#!/usr/bin/env python

"""Script for running the remote server tests using different interpreters.

Usage: run.py interpreter [arguments]

`interpreter` is the only required argument and specifies Python interpreter
to run the remote server with. The interpreter must be found from PATH or
given as an absolute path.

`arguments` are normal Robot Framework options and arguments. Test case files
are under `atest` directory.

If only the interpreter are given, all acceptance tests under `atest` directory
as well as unit tests under `utest` are executed. Unit tests are run first
and acceptance tests skipped if they fail. To run only unit tests, use
`utest/run.py` instead.

Examples:

  run.py python                      # All unit and acceptance tests with Python
  run.py "py -3" atest/kwargs.robot  # One suite with Python 3 on Windows
  run.py ipy --test NoMessage atest  # Specific test using IronPython
"""

from __future__ import print_function

from os.path import abspath, dirname, exists, join
import os
import shutil
import shlex
import sys
import subprocess

import robot
import robotstatuschecker


if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
    sys.exit(__doc__)

curdir = dirname(abspath(__file__))
results = join(curdir, 'results')
output = join(results, 'output.xml')
interpreter = sys.argv[1]
arguments = sys.argv[2:]

if exists(results):
    shutil.rmtree(results)
os.mkdir(results)

if not arguments:
    print('Running unit tests with "%s".' % interpreter)
    command = shlex.split(interpreter) + [join(curdir, 'utest', 'run.py')]
    rc = subprocess.call(command)
    print()
    if rc != 0:
        print('%d unit test%s failed.' % (rc, 's' if rc != 1 else ''))
        sys.exit(rc)
    arguments = [join(curdir, 'atest')]

excludes = []
if os.sep == '\\':
    excludes.extend(['--exclude', 'no-windows'])
if 'ipy' in interpreter:
    excludes.extend(['--exclude', 'no-ipy'])
command = [
    'python', '-m', 'robot.run',
    '--variable', 'INTERPRETER:%s' % interpreter,
    '--doc', 'Remote server tests on "%s"' % interpreter,
    '--metadata', 'Server_Interpreter:%s' % interpreter,
    '--output', output, '--log', 'NONE', '--report', 'NONE'
] + excludes + arguments
print('Running acceptance tests with command:\n%s' % ' '.join(command))
rc = subprocess.call(command)
print()
if rc > 250:
    print('Running acceptance tests failed.')
    sys.exit(rc)

print('Verifying results.')
robotstatuschecker.process_output(output)
rc = robot.rebot(output, outputdir=results, noncritical='skip')
print()
if rc == 0:
    print('All tests passed.')
else:
    print('%d acceptance test%s failed.' % (rc, 's' if rc != 1 else ''))
sys.exit(rc)
