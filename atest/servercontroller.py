#!/usr/bin/env python

"""Module/script for controlling remote server used in tests.

When used as module, provides `start`, `test`, and `stop` methods.
The server's stdin and stdout streams are redirected to results/server.txt

Usage:  servercontroller.py start|stop|test [args]

  start args: [interpreter=sys.executable] [library='StaticApiLibrary.py']
  test args:  [port=8270] [attempts=1]
  stop args:  [port=8270]

Note: Starting from CLI leaves the terminal in a messed up state.
"""

from __future__ import with_statement
import xmlrpclib
import time
import subprocess
import socket
from os.path import abspath, dirname, exists, join
import os
import sys


BASE = dirname(abspath(__file__))


def start(interpreter=sys.executable, library='StaticApiLibrary.py'):
    results = _get_result_directory()
    with open(join(results, 'server.txt'), 'w') as output:
        server = subprocess.Popen([interpreter, join(BASE, 'libs', library)],
                                  stdout=output, stderr=subprocess.STDOUT,
                                  env=_get_environ())
    if not test(attempts=15):
        server.terminate()
        raise RuntimeError('Starting remote server failed')

def _get_result_directory():
    path = join(BASE, 'results')
    if not exists(path):
        os.mkdir(path)
    return path

def _get_environ():
    environ = os.environ.copy()
    src = join(BASE, '..', 'src')
    environ.update(PYTHONPATH=src, JYTHONPATH=src, IRONPYTHONPATH=src)
    return environ


def test(port=8270, attempts=1):
    url = 'http://localhost:%s' % port
    for i in range(int(attempts)):
        if i > 0:
            time.sleep(1)
        try:
            ret = xmlrpclib.ServerProxy(url).run_keyword('get_server_language', [])
        except socket.error, (errno, errmsg):
            pass
        except xmlrpclib.Error, err:
            errmsg = err.faultString
            break
        else:
            print "%s remote server running on port %s" % (ret['return'], port)
            return True
    print "Failed to connect to remote server on port %s: %s" % (port, errmsg)
    return False


def stop(port=8270):
    if test(port):
        server = xmlrpclib.ServerProxy('http://localhost:%s' % port)
        server.stop_remote_server()
        print "Remote server on port %s stopped" % port


if __name__ == '__main__':
    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        sys.exit(__doc__)
    mode = sys.argv[1]
    args = sys.argv[2:]
    try:
        {'start': start, 'stop': stop, 'test': test}[mode](*args)
    except (KeyError, TypeError):
        sys.exit(__doc__)
