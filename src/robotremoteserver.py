#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016- Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import print_function

from collections import Mapping
from contextlib import contextmanager
import inspect
import os
import re
import signal
import sys
import threading
import traceback

if sys.version_info < (3,):
    from StringIO import StringIO
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    from xmlrpclib import Binary, ServerProxy
    PY2, PY3 = True, False
else:
    from io import StringIO
    from xmlrpc.client import Binary, ServerProxy
    from xmlrpc.server import SimpleXMLRPCServer
    PY2, PY3 = False, True
    unicode = str
    long = int


__version__ = 'devel'

BINARY = re.compile('[\x00-\x08\x0B\x0C\x0E-\x1F]')
NON_ASCII = re.compile('[\x80-\xff]')


class RobotRemoteServer(object):

    def __init__(self, library, host='127.0.0.1', port=8270, port_file=None,
                 allow_stop=True, serve=True):
        """Configure and start-up remote server.

        :param library:     Test library instance or module to host.
        :param host:        Address to listen. Use ``'0.0.0.0'`` to listen
                            to all available interfaces.
        :param port:        Port to listen. Use ``0`` to select a free port
                            automatically. Can be given as an integer or as
                            a string.
        :param port_file:   File to write port that is used. ``None`` means
                            no such file is written.
        :param allow_stop:  Allow/disallow stopping the server using ``Stop
                            Remote Server`` keyword.
        :param serve:       When ``True`` starts the server automatically.
                            When ``False``, server can be started with
                            :meth:`serve` or :meth:`start` methods.
        """
        self._server = StoppableXMLRPCServer(host, int(port), port_file,
                                             allow_stop)
        self._library = RemoteLibraryFactory(library)
        self._register_functions(self._server)
        if serve:
            self.serve()

    @property
    def server_address(self):
        """Server address as a tuple ``(host, port)``."""
        return self._server.server_address

    @property
    def server_port(self):
        """Server port as an integer."""
        return self._server.server_address[1]

    def _register_functions(self, server):
        server.register_function(self.get_keyword_names)
        server.register_function(self.run_keyword)
        server.register_function(self.get_keyword_arguments)
        server.register_function(self.get_keyword_documentation)
        server.register_function(self._stop_serve, 'stop_remote_server')

    def serve(self, log=True):
        """Start the server and wait for it to finish.

        :param log:  Log message about startup or not.

        If this method is called in the main thread, automatically registers
        signals INT, TERM and HUP to stop the server.

        Using this method requires using ``serve=False`` when initializing the
        server. Using ``serve=True`` is equal to first using ``serve=False``
        and then calling this method. Alternatively :meth:`start` can be used
        to start the server on background.

        In addition to signals, the server can be stopped with ``Stop Remote
        Server`` keyword. Using :meth:`stop` method is possible too, but
        requires running this method in a thread.
        """
        self._server.serve(log=log)

    def start(self, log=False):
        """Start the server on background.

        :param log:  Log message about startup or not.

        Started server can be stopped with :meth:`stop` method. Stopping is
        not possible by using signals or ``Stop Remote Server`` keyword.
        """
        self._server.start(log=log)

    def stop(self, log=False):
        """Start the server.

        :param log:  Log message about stopping or not.
        """
        self._server.stop(log=log)

    def _stop_serve(self, log=True):
        return self._server.stop_serve(remote=True, log=log)

    def _log(self, msg, level=None):
        if level:
            msg = '*%s* %s' % (level.upper(), msg)
        self._write_to_stream(msg, sys.stdout)
        if sys.__stdout__ is not sys.stdout:
            self._write_to_stream(msg, sys.__stdout__)

    def _write_to_stream(self, msg, stream):
        stream.write(msg + '\n')
        stream.flush()

    def get_keyword_names(self):
        return self._library.get_keyword_names() + ['stop_remote_server']

    def run_keyword(self, name, args, kwargs=None):
        if name == 'stop_remote_server':
            return KeywordRunner(self._stop_serve).run_keyword(args, kwargs)
        return self._library.run_keyword(name, args, kwargs)

    def get_keyword_arguments(self, name):
        if name == 'stop_remote_server':
            return ['log=True']
        return self._library.get_keyword_arguments(name)

    def get_keyword_documentation(self, name):
        if name == 'stop_remote_server':
            return ('Stop the remote server unless stopping is disabled.\n\n'
                    'Return ``True/False`` depending was server stopped or not.')
        return self._library.get_keyword_documentation(name)


class StoppableXMLRPCServer(SimpleXMLRPCServer):
    allow_reuse_address = True

    def __init__(self, host, port, port_file=None, allow_remote_stop=True):
        SimpleXMLRPCServer.__init__(self, (host, port), logRequests=False,
                                    bind_and_activate=False)
        self._port_file = port_file
        self._thread = None
        self._allow_remote_stop = allow_remote_stop
        self._stop_serve = None
        self._stop_lock = threading.Lock()

    def serve(self, log=True):
        self._stop_serve = threading.Event()
        with self._stop_signals():
            self.start(log)
            while not self._stop_serve.is_set():
                self._stop_serve.wait(1)
            self._stop_serve = None
            self.stop(log)

    @contextmanager
    def _stop_signals(self):
        original = {}
        stop = lambda signum, frame: self.stop_serve(remote=False)
        try:
            for name in 'SIGINT', 'SIGTERM', 'SIGHUP':
                if hasattr(signal, name):
                    original[name] = signal.signal(getattr(signal, name), stop)
        except ValueError:  # Not in main thread
            pass
        try:
            yield
        finally:
            for name in original:
                signal.signal(getattr(signal, name), original[name])

    def stop_serve(self, remote=True, log=True):
        if (self._allow_remote_stop or not remote) and self._stop_serve:
            self._stop_serve.set()
            return True
        # TODO: Log to __stdout__? WARN?
        self._log('does not allow stopping', log)
        return False

    def start(self, log=False):
        self.server_bind()
        self.server_activate()
        self._thread = threading.Thread(target=self.serve_forever)
        self._thread.daemon = True
        self._thread.start()
        self._announce_start(log, self._port_file)

    def _announce_start(self, log_start, port_file):
        self._log('started', log_start)
        if port_file:
            with open(port_file, 'w') as pf:
                pf.write(str(self.server_address[1]))

    def stop(self, log=False):
        if self._stop_serve:
            return self.stop_serve(log=log)
        with self._stop_lock:
            if not self._thread:  # already stopped
                return
            self.shutdown()
            self.server_close()
            self._thread.join()
            self._thread = None
            self._announce_stop(log, self._port_file)

    def _announce_stop(self, log_end, port_file):
        self._log('stopped', log_end)
        if port_file and os.path.exists(port_file):
            os.remove(port_file)    # TODO: Document that port file is removed

    def _log(self, action, log=True):
        if log:
            host, port = self.server_address
            print ('Robot Framework remote server at %s:%s %s.'
                   % (host, port, action))


def RemoteLibraryFactory(library):
    if inspect.ismodule(library):
        return StaticRemoteLibrary(library)
    get_keyword_names = dynamic_method(library, 'get_keyword_names')
    if not get_keyword_names:
        return StaticRemoteLibrary(library)
    run_keyword = dynamic_method(library, 'run_keyword')
    if not run_keyword:
        return HybridRemoteLibrary(library, get_keyword_names)
    return DynamicRemoteLibrary(library, get_keyword_names, run_keyword)


def dynamic_method(library, underscore_name):
    tokens = underscore_name.split('_')
    camelcase_name = tokens[0] + ''.join(t.title() for t in tokens[1:])
    for name in underscore_name, camelcase_name:
        method = getattr(library, name, None)
        if method and is_function_or_method(method):
            return method
    return None


def is_function_or_method(item):
    return inspect.isfunction(item) or inspect.ismethod(item)


class StaticRemoteLibrary(object):

    def __init__(self, library):
        self._library = library
        self._names, self._robot_name_index = self._get_keyword_names(library)

    def _get_keyword_names(self, library):
        names = []
        robot_name_index = {}
        for name, kw in inspect.getmembers(library):
            if is_function_or_method(kw):
                if getattr(kw, 'robot_name', None):
                    names.append(kw.robot_name)
                    robot_name_index[kw.robot_name] = name
                elif name[0] != '_':
                    names.append(name)
        return names, robot_name_index

    def get_keyword_names(self):
        return self._names

    def run_keyword(self, name, args, kwargs=None):
        kw = self._get_keyword(name)
        return KeywordRunner(kw).run_keyword(args, kwargs)

    def _get_keyword(self, name):
        if name in self._robot_name_index:
            name = self._robot_name_index[name]
        return getattr(self._library, name)

    def get_keyword_arguments(self, name):
        if __name__ == '__init__':
            return []
        kw = self._get_keyword(name)
        args, varargs, kwargs, defaults = inspect.getargspec(kw)
        if inspect.ismethod(kw):
            args = args[1:]  # drop 'self'
        if defaults:
            args, names = args[:-len(defaults)], args[-len(defaults):]
            args += ['%s=%s' % (n, d) for n, d in zip(names, defaults)]
        if varargs:
            args.append('*%s' % varargs)
        if kwargs:
            args.append('**%s' % kwargs)
        return args

    def get_keyword_documentation(self, name):
        if name == '__intro__':
            return inspect.getdoc(self._library) or ''
        if name == '__init__':
            init = self._get_init(self._library)
            return inspect.getdoc(init) or ''
        keyword = self._get_keyword(name)
        doc = (inspect.getdoc(keyword) or '').lstrip()
        if getattr(keyword, 'robot_tags', []):
            tags = 'Tags: %s' % ', '.join(keyword.robot_tags)
            doc = '%s\n\n%s' % (doc, tags) if doc else tags
        return doc

    def _get_init(self, library):
        if inspect.ismodule(library):
            return None
        init = getattr(library, '__init__', None)
        return init if self._is_valid_init(init) else None

    def _is_valid_init(self, init):
        if not init:
            return False
        # https://bitbucket.org/pypy/pypy/issues/2462/
        if 'PyPy' in sys.version:
            if PY2:
                return init.__func__ is not object.__init__.__func__
            return init is not object.__init__
        return is_function_or_method(init)


class HybridRemoteLibrary(StaticRemoteLibrary):

    def __init__(self, library, get_keyword_names):
        StaticRemoteLibrary.__init__(self, library)
        self.get_keyword_names = get_keyword_names


class DynamicRemoteLibrary(HybridRemoteLibrary):

    def __init__(self, library, get_keyword_names, run_keyword):
        HybridRemoteLibrary.__init__(self, library, get_keyword_names)
        self._run_keyword = run_keyword
        self._supports_kwargs = self._get_kwargs_support(run_keyword)
        self._get_keyword_arguments \
            = dynamic_method(library, 'get_keyword_arguments')
        self._get_keyword_documentation \
            = dynamic_method(library, 'get_keyword_documentation')

    def _get_kwargs_support(self, run_keyword):
        spec = inspect.getargspec(run_keyword)
        return len(spec.args) > 3    # self, name, args, kwargs=None

    def run_keyword(self, name, args, kwargs=None):
        args = [name, args, kwargs] if kwargs else [name, args]
        return KeywordRunner(self._run_keyword).run_keyword(args)

    def get_keyword_arguments(self, name):
        if self._get_keyword_arguments:
            return self._get_keyword_arguments(name)
        if self._supports_kwargs:
            return ['*varargs', '**kwargs']
        return ['*varargs']

    def get_keyword_documentation(self, name):
        if self._get_keyword_documentation:
            return self._get_keyword_documentation(name)
        return ''


class KeywordRunner(object):

    def __init__(self, keyword):
        self._keyword = keyword

    def run_keyword(self, args, kwargs=None):
        args = self._handle_binary(args)
        kwargs = self._handle_binary(kwargs or {})
        result = KeywordResult()
        with StandardStreamInterceptor() as interceptor:
            try:
                return_value = self._keyword(*args, **kwargs)
            except Exception:
                result.set_error(*sys.exc_info())
            else:
                try:
                    result.set_return(return_value)
                except Exception:
                    result.set_error(*sys.exc_info()[:2])
                else:
                    result.set_status('PASS')
        result.set_output(interceptor.output)
        return result.data

    def _handle_binary(self, arg):
        # No need to compare against other iterables or mappings because we
        # only get actual lists and dicts over XML-RPC. Binary cannot be
        # a dictionary key either.
        if isinstance(arg, list):
            return [self._handle_binary(item) for item in arg]
        if isinstance(arg, dict):
            return dict((key, self._handle_binary(arg[key])) for key in arg)
        if isinstance(arg, Binary):
            return arg.data
        return arg


class StandardStreamInterceptor(object):

    def __init__(self):
        self.output = ''
        self.origout = sys.stdout
        self.origerr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        stdout = sys.stdout.getvalue()
        stderr = sys.stderr.getvalue()
        close = [sys.stdout, sys.stderr]
        sys.stdout = self.origout
        sys.stderr = self.origerr
        for stream in close:
            stream.close()
        if stdout and stderr:
            if not stderr.startswith(('*TRACE*', '*DEBUG*', '*INFO*', '*HTML*',
                                      '*WARN*', '*ERROR*')):
                stderr = '*INFO* %s' % stderr
            if not stdout.endswith('\n'):
                stdout += '\n'
        self.output = stdout + stderr


class KeywordResult(object):
    _generic_exceptions = (AssertionError, RuntimeError, Exception)

    def __init__(self):
        self.data = {'status': 'FAIL'}

    def set_error(self, exc_type, exc_value, exc_tb=None):
        self.data['error'] = self._get_message(exc_type, exc_value)
        if exc_tb:
            self.data['traceback'] = self._get_traceback(exc_tb)
        continuable = self._get_error_attribute(exc_value, 'CONTINUE')
        if continuable:
            self.data['continuable'] = continuable
        fatal = self._get_error_attribute(exc_value, 'EXIT')
        if fatal:
            self.data['fatal'] = fatal

    def _get_message(self, exc_type, exc_value):
        name = exc_type.__name__
        message = self._get_message_from_exception(exc_value)
        if not message:
            return name
        if exc_type in self._generic_exceptions \
                or getattr(exc_value, 'ROBOT_SUPPRESS_NAME', False):
            return message
        return '%s: %s' % (name, message)

    def _get_message_from_exception(self, value):
        # UnicodeError occurs if message contains non-ASCII bytes
        try:
            msg = unicode(value)
        except UnicodeError:
            msg = ' '.join(self._str(a, handle_binary=False) for a in value.args)
        return self._handle_binary_result(msg)

    def _get_traceback(self, exc_tb):
        # Latest entry originates from this module so it can be removed
        entries = traceback.extract_tb(exc_tb)[1:]
        trace = ''.join(traceback.format_list(entries))
        return 'Traceback (most recent call last):\n' + trace

    def _get_error_attribute(self, exc_value, name):
        return bool(getattr(exc_value, 'ROBOT_%s_ON_FAILURE' % name, False))

    def set_return(self, value):
        value = self._handle_return_value(value)
        if value != '':
            self.data['return'] = value

    def _handle_return_value(self, ret):
        if isinstance(ret, (str, unicode, bytes)):
            return self._handle_binary_result(ret)
        if isinstance(ret, (int, long, float)):
            return ret
        if isinstance(ret, Mapping):
            return dict((self._str(key), self._handle_return_value(value))
                        for key, value in ret.items())
        try:
            return [self._handle_return_value(item) for item in ret]
        except TypeError:
            return self._str(ret)

    def _handle_binary_result(self, result):
        if not self._contains_binary(result):
            return result
        if not isinstance(result, bytes):
            try:
                result = result.encode('ASCII')
            except UnicodeError:
                raise ValueError("Cannot represent %r as binary." % result)
        # With IronPython Binary cannot be sent if it contains "real" bytes.
        if sys.platform == 'cli':
            result = str(result)
        return Binary(result)

    def _contains_binary(self, result):
        if PY3:
            return isinstance(result, bytes) or BINARY.search(result)
        return (isinstance(result, bytes) and NON_ASCII.search(result) or
                BINARY.search(result))

    def _str(self, item, handle_binary=True):
        if item is None:
            return ''
        if not isinstance(item, (str, unicode, bytes)):
            item = unicode(item)
        if handle_binary:
            item = self._handle_binary_result(item)
        return item

    def set_status(self, status):
        self.data['status'] = status

    def set_output(self, output):
        if output:
            self.data['output'] = self._handle_binary_result(output)


def test_remote_server(uri, log=True):
    """Test is remote server running.

    :param uri:  Server address.
    :param log:  Log status message or not.
    :return      ``True`` if server is running, ``False`` otherwise.
    """
    try:
        ServerProxy(uri).get_keyword_names()
    except Exception:
        if log:
            print('No remote server running at %s.' % uri)
        return False
    if log:
        print('Remote server running at %s.' % uri)
    return True


def stop_remote_server(uri, log=True):
    """Stop remote server.

    :param uri:  Server address.
    :param log:  Log status message or not.
    :return      ``True`` if server was stopped or it was not running in
                 the first place, ``False`` otherwise.
    """
    if not test_remote_server(uri, log=False):
        if log:
            print('No remote server running at %s.' % uri)
        return True
    if log:
        print('Stopping remote server at %s.' % uri)
    args = [] if log else [False]
    return ServerProxy(uri).stop_remote_server(*args)


if __name__ == '__main__':

    def parse_args(script, *args):
        actions = {'stop': stop_remote_server, 'test': test_remote_server}
        if not (0 < len(args) < 3) or args[0] not in actions:
            sys.exit('Usage:  %s {test|stop} [uri]' % os.path.basename(script))
        uri = args[1] if len(args) == 2 else 'http://127.0.0.1:8270'
        if '://' not in uri:
            uri = 'http://' + uri
        return actions[args[0]], uri

    action, uri = parse_args(*sys.argv)
    action(uri)
