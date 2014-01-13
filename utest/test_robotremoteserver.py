#!/usr/bin/env python

import unittest
import sys

from robotremoteserver import RobotRemoteServer


class NonServingRemoteServer(RobotRemoteServer):
    def __init__(self, library):
        self._library = library

class StaticLibrary:
    def passing_keyword(self):
        pass
    def failing_keyword(self, exception, message='Hello, world!'):
        raise exception(message)
    def logging_keyword(self, stdout, stderr):
        if stdout:
            sys.stdout.write(stdout)
        if stderr:
            sys.stderr.write(stderr)
        self.streams = (sys.stdout, sys.stderr)
    def _not_included(self):
        """Starts with an underscore"""
    not_included = "Not a method or function"
    not_included_2 = NonServingRemoteServer  # Callable but not method/function

class HybridLibrary:
    def __init__(self):
        self.library = StaticLibrary()
    def get_keyword_names(self):
        return [n for n in dir(self.library) if n.endswith('_keyword')]
    def __getattr__(self, name):
        return getattr(self.library, name)
    def not_included(self):
        """Not returned by get_keyword_names"""


class TestStaticApi(unittest.TestCase):
    library = StaticLibrary()

    def setUp(self):
        self.server = NonServingRemoteServer(self.library)

    def test_get_keyword_names(self):
        self.assertEquals(self.server.get_keyword_names(),
                          ['failing_keyword', 'logging_keyword',
                           'passing_keyword', 'stop_remote_server'])

    def test_run_passing_keyword(self):
        self.assertEquals(self.server.run_keyword('passing_keyword', []),
                          {'status': 'PASS', 'output': '', 'traceback': '',
                           'return': '', 'error': ''})

    def test_run_failing_keyword(self):
        ret = self.server.run_keyword('failing_keyword', [ValueError])
        self.assertEquals(ret['status'], 'FAIL')
        self.assertEquals(ret['error'], 'ValueError: Hello, world!')

    def test_strip_generic_exception_names_from_error_messages(self):
        for exception in AssertionError, Exception, RuntimeError:
            ret = self.server.run_keyword('failing_keyword', [exception])
            self.assertEquals(ret['status'], 'FAIL')
            self.assertEquals(ret['error'], 'Hello, world!')

    def test_return_only_exception_name_if_no_error_message(self):
        for exception in AssertionError, ValueError:
            ret = self.server.run_keyword('failing_keyword', [exception, ''])
            self.assertEquals(ret['status'], 'FAIL')
            self.assertEquals(ret['error'], exception.__name__)

    def test_logging_to_stdout(self):
        ret = self.server.run_keyword('logging_keyword', ['out', ''])
        self.assertEquals(ret['output'], 'out')
        self.assertTrue(all(s.closed for s in self.library.streams))

    def test_logging_to_stderr(self):
        ret = self.server.run_keyword('logging_keyword', ['', 'err'])
        self.assertEquals(ret['output'], 'err')
        self.assertTrue(all(s.closed for s in self.library.streams))

    def test_logging_to_stdout_and_stderr(self):
        ret = self.server.run_keyword('logging_keyword', ['out', 'err'])
        self.assertEquals(ret['output'], 'out\n*INFO* err')
        self.assertTrue(all(s.closed for s in self.library.streams))


class TestHybridApi(TestStaticApi):
    library = HybridLibrary()


if __name__ == '__main__':
    unittest.main()
