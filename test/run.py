#!/usr/bin/env python

"""Script for running the remote server tests using different interpreters.

Usage: run.py interpreter [arguments]

`interpreter` is the only required argument and specifies Python interpreter
to run the server with. The interpreter must be found from PATH or given as
an absolute path. Notice that on Windows you must use `jython.bat` not just
`jython`.

`arguments` are normal Robot Framework options and arguments. Test case files
are under `atest` directory.

If only the interpreter are given, all acceptance tests under `atest` directory
as well as unit tests under `utest` are executed. Unit tests are run first
and acceptance tests skipped if they fail. To run only unit tests, use
`utest/run.py` instead.

Examples:

  run.py python                      # All unit and acceptance tests with Python
  run.py jython.bat atest            # All acceptance tests w/ Jython on Windows
  run.py jython atest/logging.robot  # One suite with Jython outside Windows
  run.py ipy --test NoMessage atest  # Specific test using IronPython
"""

import sys
import subprocess
from os.path import abspath, basename, dirname, exists, join, splitext
from os import mkdir
from shutil import rmtree

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
    rmtree(results)
mkdir(results)

if not arguments:
    print('Running unit tests with %s.' % interpreter)
    rc = subprocess.call([interpreter, join(curdir, 'utest', 'run.py')])
    if rc != 0:
        print('%d unit test%s failed.' % (rc, 's' if rc != 1 else ''))
        sys.exit(rc)
    arguments = [join(curdir, 'atest')]

command = ['python', '-m', 'robot.run',
           '--variable', 'INTERPRETER:%s' % interpreter,
           '--name', '%s Remote Server' % splitext(basename(interpreter))[0].title(),
           '--metadata', 'Server_Interpreter:%s' % interpreter,
           '--noncritical', 'skip',
           '--output', output, '--log', 'NONE', '--report', 'NONE'] + arguments
print('Running acceptance tests with command:\n%s' % ' '.join(command))
subprocess.call(command)

print('Verifying results.')
robotstatuschecker.process_output(output)
rc = robot.rebot(output, outputdir=results, noncritical='skip')
if rc == 0:
    print('All tests passed.')
else:
    print('%d acceptance test%s failed.' % (rc, 's' if rc != 1 else ''))
sys.exit(rc)
