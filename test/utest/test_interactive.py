from contextlib import contextmanager
import sys
import threading
import time
import unittest

from robot.libraries.Remote import Remote

from robotremoteserver import (RobotRemoteServer, StringIO,
                               stop_remote_server, test_remote_server)


class Library(object):

    def kw(self):
        print('The message!')
        return 42


class TesInteractiveUsage(unittest.TestCase):

    def setUp(self):
        self.server = RobotRemoteServer(Library(), port=0, serve=False)

    def test_serve(self):
        self.assertEqual(self.server.server_address[1], 0)
        with self._server_thread():
            uri = self._wait_until_started()
            try:
                self._run_remote_keyword(uri)
            finally:
                self.server.stop(log=False)
            self._wait_until_stopped(uri)
            self.assertEqual(test_remote_server(uri, log=False), False)
            self.server.stop(log=False)

    @contextmanager
    def _server_thread(self):
        thread = threading.Thread(target=self.server.serve,
                                  kwargs={'log': False})
        thread.start()
        try:
            yield
        finally:
            self.server.stop(log=False)
            thread.join()

    def _wait_until_started(self, timeout=5):
        start_time = time.time()
        while time.time() < start_time + timeout:
            if self.server.server_port != 0:
                return 'http://%s:%s' % self.server.server_address
            time.sleep(0.01)
        raise AssertionError('Server did not start in %s seconds.' % timeout)

    def _run_remote_keyword(self, uri):
        origout = sys.stdout
        sys.stdout = StringIO()
        try:
            self.assertEqual(Remote(uri).run_keyword('kw', (), None), 42)
            self.assertEqual(sys.stdout.getvalue(), 'The message!\n')
        finally:
            sys.stdout.close()
            sys.stdout = origout

    def _wait_until_stopped(self, uri, timeout=5):
        start_time = time.time()
        while time.time() < start_time + timeout:
            if not test_remote_server(uri, log=False):
                return
            time.sleep(0.01)
        self.server.stop()
        raise AssertionError('Server did not stop in %s seconds.' % timeout)

    def test_start_and_stop(self):
        self.server.start()
        uri = 'http://%s:%s' % self.server.server_address
        try:
            self._run_remote_keyword(uri)
        finally:
            self.server.stop()
        self.assertEqual(test_remote_server(uri, log=False), False)

    def test_stop_remote_server_works_with_serve(self):
        with self._server_thread():
            uri = self._wait_until_started()
            self.assertEqual(test_remote_server(uri, log=False), True)
            self.assertEqual(stop_remote_server(uri, log=False), True)
            self._wait_until_stopped(uri)
            self.assertEqual(stop_remote_server(uri, log=False), True)

    def test_stop_remote_server_wont_work_with_start(self):
        self.server.start()
        uri = 'http://%s:%s' % self.server.server_address
        try:
            self.assertEqual(test_remote_server(uri, log=False), True)
            self.assertEqual(stop_remote_server(uri, log=False), False)
            self.assertEqual(test_remote_server(uri, log=False), True)
        finally:
            self.server.stop()
        self.assertEqual(test_remote_server(uri, log=False), False)


if __name__ == '__main__':
    unittest.main()
