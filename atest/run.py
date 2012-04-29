#!/usr/bin/env python

"""Script for running the remote server tests using different interpreters.

usage: run.py server[:runner] [[options] datasources]

`server` is the only required argument and specifies the server interpreter
to use. `runner` is the interpreter to use for running tests, defaulting to
the server interpreter.

By default all tests under `tests` directory are executed. This can be
changed by giving data sources and options explicitly.
"""

import sys
import subprocess
from os.path import abspath, dirname, exists, join
from os import mkdir
from shutil import rmtree

import robot

import servercontroller
import statuschecker

BASE = dirname(abspath(__file__))
RESULTS = join(BASE, 'results')
OUTPUT = join(RESULTS, 'output.xml')
if exists(RESULTS):
    rmtree(RESULTS)
mkdir(RESULTS)


if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
    sys.exit(__doc__)

interpreters = sys.argv[1]
if ':' in interpreters:
    server_interpreter, runner_interpreter = interpreters.rsplit(':', 1)
else:
    server_interpreter = runner_interpreter = interpreters

servercontroller.start(server_interpreter)

args = [runner_interpreter, '-m', 'robot.run', '--name', interpreters,
        '--output', OUTPUT, '--log', 'NONE', '--report', 'NONE']
args.extend(sys.argv[2:] or [join(BASE, 'tests')])
print 'Running tests with command:\n%s' % ' '.join(args)
subprocess.call(args)

servercontroller.stop()
print
statuschecker.process_output(OUTPUT)
rc = robot.rebot(OUTPUT, outputdir=RESULTS)
if rc == 0:
    print 'All tests passed'
else:
    print '%d test%s failed' % (rc, 's' if rc != 1 else '')
