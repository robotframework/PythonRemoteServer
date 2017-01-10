#!/usr/bin/env python

import unittest
import sys

from robotremoteserver import RobotRemoteServer, RemoteLibrary


class NonServingRemoteServer(RobotRemoteServer):

    def __init__(self, library):
        self._library = RemoteLibrary(library)


class StaticLibrary:

    def passing_keyword(self):
        pass

    def failing_keyword(self, exception=AssertionError, message='Hello, world!',
                        **kwargs):
        err = exception(message)
        for name, value in kwargs.items():
            setattr(err, name, value)
        raise err

    def returning_keyword(self, value):
        return value

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
                           'passing_keyword', 'returning_keyword',
                           'stop_remote_server'])

    def test_run_passing_keyword(self):
        self.assertEquals(self._run('passing_keyword'), {'status': 'PASS'})

    def test_returning_keyword(self):
        for ret in 'Hello, world!', 42, True:
            self.assertEquals(self._run('returning_keyword', ret),
                              {'status': 'PASS', 'return': ret})

    def test_run_failing_keyword(self):
        ret = self._run('failing_keyword', ValueError)
        self._verify_failed(ret, 'ValueError: Hello, world!')

    def test_strip_generic_exception_names_from_error_messages(self):
        for exception in AssertionError, Exception, RuntimeError:
            ret = self._run('failing_keyword', exception)
            self._verify_failed(ret, 'Hello, world!')

    def test_return_only_exception_name_if_no_error_message(self):
        for exception in AssertionError, ValueError:
            ret = self._run('failing_keyword', exception, '')
            self._verify_failed(ret, exception.__name__)

    def test_continuable_error(self):
        ret = self._run('failing_keyword', ROBOT_CONTINUE_ON_FAILURE=True)
        self._verify_failed(ret, continuable=True)

    def test_fatal_error(self):
        ret = self._run('failing_keyword', ROBOT_EXIT_ON_FAILURE='yes please')
        self._verify_failed(ret, fatal=True)

    def test_logging_to_stdout(self):
        ret = self._run('logging_keyword', 'out', '')
        self._verify_logged(ret, 'out')

    def test_logging_to_stderr(self):
        ret = self._run('logging_keyword', '', 'err')
        self._verify_logged(ret, 'err')

    def test_logging_to_stdout_and_stderr(self):
        ret = self._run('logging_keyword', 'out', 'err')
        self._verify_logged(ret, 'out\n*INFO* err')

    def _run(self, kw, *args, **kwargs):
        return self.server.run_keyword(kw, args, kwargs)

    def _verify_failed(self, ret, error='Hello, world!', continuable=False,
                       fatal=False):
        ret.pop('traceback')
        if continuable:
            self.assertEquals(ret.pop('continuable'), True)
        if fatal:
            self.assertEquals(ret.pop('fatal'), True)
        self.assertEquals(ret, {'error': error, 'status': 'FAIL'})

    def _verify_logged(self, ret, output):
        self.assertEquals(ret, {'output': output, 'status': 'PASS'})
        self.assertTrue(all(s.closed for s in self.library.streams))


class TestHybridApi(TestStaticApi):
    library = HybridLibrary()


if __name__ == '__main__':
    unittest.main()
