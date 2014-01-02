#!/usr/bin/env python

"""Script for running the remote server tests using different interpreters.

Usage: run.py interpreter [[options] datasources]

`interpreter` is the only required argument and specifies the Python
interpreter to run the server with.

By default all tests under `tests` directory are executed. This can be
changed by giving data sources and options explicitly.
"""

import sys
import subprocess
from os.path import abspath, dirname, exists, join
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
arguments = sys.argv[2:] or [join(curdir, 'tests')]

if exists(results):
    rmtree(results)
mkdir(results)

command = ['python', '-m', 'robot.run',
           '--variable', 'INTERPRETER:%s' % interpreter,
           '--name', '%s Remote Server' % interpreter.title(),
           '--output', output, '--log', 'NONE', '--report', 'NONE'] + arguments
print 'Running tests with command:\n%s' % ' '.join(command)
subprocess.call(command)

print
robotstatuschecker.process_output(output)
rc = robot.rebot(output, outputdir=results)
if rc == 0:
    print 'All tests passed.'
else:
    print '%d test%s failed.' % (rc, 's' if rc != 1 else '')
