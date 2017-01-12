from contextlib import contextmanager
import threading
import time
import unittest

from robot.libraries.Remote import Remote

from robotremoteserver import (RobotRemoteServer, stop_remote_server,
                               test_remote_server)


class Library(object):

    def kw(self):
        return 42


class TesInteractiveUsage(unittest.TestCase):

    def setUp(self):
        self.server = RobotRemoteServer(Library(), port=0, serve=False)

    def test_serve(self):
        self.assertEqual(self.server.server_address[1], 0)
        with self._server_thread():
            uri = self._wait_until_started()
            try:
                self.assertEqual(Remote(uri).run_keyword('kw', (), None), 42)
            finally:
                self.assertEqual(self.server.stop_serve(log=False), True)
            self._wait_until_stopped(uri)
            self.assertEqual(self.server.stop_serve(log=False), True)
            self.assertEqual(test_remote_server(uri, log=False), False)

    @contextmanager
    def _server_thread(self):
        thread = threading.Thread(target=self.server.serve,
                                  kwargs={'log': False})
        thread.start()
        try:
            yield
        finally:
            self.server.force_stop_serve(log=False)
            thread.join()

    def _wait_until_started(self, timeout=5):
        start_time = time.time()
        while time.time() < start_time + timeout:
            if self.server.server_port != 0:
                return 'http://%s:%s' % self.server.server_address
            time.sleep(0.01)
        raise AssertionError('Server did not start in %s seconds.' % timeout)

    def _wait_until_stopped(self, uri, timeout=5):
        start_time = time.time()
        while time.time() < start_time + timeout:
            if not test_remote_server(uri, log=False):
                return
            time.sleep(0.01)
        self.server.stop_serve()
        raise AssertionError('Server did not stop in %s seconds.' % timeout)

    def test_start_and_stop(self):
        self.server.start()
        uri = 'http://%s:%s' % self.server.server_address
        try:
            self.assertEqual(Remote(uri).run_keyword('kw', (), None), 42)
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

    def test_stop_remote_server_can_be_disabled_with_serve(self):
        self.server = RobotRemoteServer(Library(), port=0, serve=False,
                                        allow_stop=False)
        with self._server_thread():
            uri = self._wait_until_started()
            self.assertEqual(test_remote_server(uri, log=False), True)
            self.assertEqual(stop_remote_server(uri, log=False), False)
            self.assertEqual(test_remote_server(uri, log=False), True)
            self.assertEqual(self.server.stop_serve(log=False), False)
            self.assertEqual(test_remote_server(uri, log=False), True)
            self.assertEqual(self.server.force_stop_serve(log=False), True)
            self._wait_until_stopped(uri)

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
