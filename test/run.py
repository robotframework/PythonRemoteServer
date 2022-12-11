#!/usr/bin/env python3

"""Script for running the remote server tests using different interpreters.

Usage: run.py [interpreter] [arguments]

`interpreter` is name or path of the Python interpreter to run the remote
server with. The interpreter must be found from PATH or given as an absolute
path. If not given, `python` will be used by default.

`arguments` are normal Robot Framework options and arguments. Test case files
are under the `atest` directory.

If no arguments are given, all acceptance tests under the `atest` directory
as well as unit tests under `utest` are executed. Unit tests are run first
and acceptance tests skipped if they fail.

If arguments are given, unit tests are not run. To run only unit tests, use
`test/utest/run.py` instead.

This script must be run using Python 3.

Examples:
  run.py                             # All unit and acceptance tests with Python
  run.py "py -3" atest/kwargs.robot  # One suite with Python 3 on Windows
  run.py ipy --test NoMessage atest  # Specific test using IronPython
"""

from os.path import abspath, dirname, exists, join
import os
import shutil
import shlex
import sys
import subprocess

import robot
import robotstatuschecker


if '-h' in sys.argv or '--help' in sys.argv:
    sys.exit(__doc__)

curdir = dirname(abspath(__file__))
results = join(curdir, 'results')
output = join(results, 'output.xml')
interpreter = shlex.split(sys.argv[1] if len(sys.argv) > 1 else 'python')
version = subprocess.check_output(interpreter + ['-V'], encoding='UTF-8',
                                  stderr=subprocess.STDOUT).strip()
py2 = version.split()[1][:3] == '2.7'
arguments = sys.argv[2:]

if exists(results):
    shutil.rmtree(results)
os.mkdir(results)

print(f'Running tests on {version}.\n')

if not arguments:
    command = interpreter + [join(curdir, 'utest', 'run.py')]
    print('Running unit tests:\n' + ' '.join(command))
    rc = subprocess.call(command)
    print()
    if rc != 0:
        tests = 'tests' if rc != 1 else 'test'
        print(f'{rc} unit {tests} failed.')
        sys.exit(rc)
    arguments = [join(curdir, 'atest')]

excludes = []
if os.sep == '\\':
    excludes.extend(['--exclude', 'no-windows'])
if 'ipy' in interpreter[0]:
    excludes.extend(['--exclude', 'no-ipy'])
command = [
    'python', '-m', 'robot.run',
    '--variable', f'INTERPRETER:{subprocess.list2cmdline(interpreter)}',
    '--variable', f'PY2:{py2}',
    '--metadata', f'Interpreter:{version}',
    '--output', output, '--log', 'NONE', '--report', 'NONE'
] + excludes + arguments
print('Running acceptance tests:\n' + ' '.join(command))
rc = subprocess.call(command)
print()
if rc > 250:
    print('Running acceptance tests failed.')
    sys.exit(rc)

print('Verifying results.')
robotstatuschecker.process_output(output)
rc = robot.rebot(output, outputdir=results)
print()
if rc == 0:
    print('All tests passed.')
else:
    tests = 'tests' if rc != 1 else 'test'
    print(f'{rc} acceptance {tests} failed.')
sys.exit(rc)
