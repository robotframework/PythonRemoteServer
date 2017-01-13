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
import errno
import inspect
import re
import signal
import select
import sys
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
    allow_reuse_address = True

    def __init__(self, library, host='127.0.0.1', port=8270, port_file=None,
                 allow_stop=True):
        """Configure and start-up remote server.

        :param library:     Test library instance or module to host.
        :param host:        Address to listen. Use ``'0.0.0.0'`` to listen
                            to all available interfaces.
        :param port:        Port to listen. Use ``0`` to select a free port
                            automatically. Can be given as an integer or as
                            a string.
        :param port_file:   File to write port that is used. ``None`` means
                            no such file is written.
        :param allow_stop:  Allow/disallow stopping the server using
                            ``Stop Remote Server`` keyword.
        """
        self._server = StoppableXMLRPCServer(host, int(port))
        self._library = RemoteLibraryFactory(library)
        self._allow_stop = allow_stop
        self._register_functions(self._server)
        self._register_signal_handlers()
        self._announce_start(port_file)
        self._server.start()

    @property
    def server_address(self):
        return self._server.server_address

    def _register_functions(self, server):
        server.register_function(self.get_keyword_names)
        server.register_function(self.run_keyword)
        server.register_function(self.get_keyword_arguments)
        server.register_function(self.get_keyword_documentation)
        server.register_function(self.stop_remote_server)

    def _register_signal_handlers(self):
        def stop_with_signal(signum, frame):
            self._allow_stop = True
            self.stop_remote_server()
        for name in 'SIGINT', 'SIGTERM', 'SIGHUP':
            if hasattr(signal, name):
                signal.signal(getattr(signal, name), stop_with_signal)

    def _announce_start(self, port_file=None):
        host, port = self.server_address
        self._log('Robot Framework remote server at %s:%s starting.'
                  % (host, port))
        if port_file:
            with open(port_file, 'w') as pf:
                pf.write(str(port))

    def stop_remote_server(self):
        prefix = 'Robot Framework remote server at %s:%s ' % self.server_address
        if self._allow_stop:
            self._log(prefix + 'stopping.')
            self._server.stop()
            return True
        self._log(prefix + 'does not allow stopping.', 'WARN')
        return False

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
            return KeywordRunner(self.stop_remote_server).run_keyword(args, kwargs)
        return self._library.run_keyword(name, args, kwargs)

    def get_keyword_arguments(self, name):
        if name == 'stop_remote_server':
            return []
        return self._library.get_keyword_arguments(name)

    def get_keyword_documentation(self, name):
        if name == 'stop_remote_server':
            return ('Stop the remote server unless stopping is disabled.\n\n'
                    'Return ``True/False`` depending was server stopped or not.')
        return self._library.get_keyword_documentation(name)


class StoppableXMLRPCServer(SimpleXMLRPCServer):
    allow_reuse_address = True

    def __init__(self, host, port):
        SimpleXMLRPCServer.__init__(self, (host, port), logRequests=False)
        self._shutdown = False

    def start(self):
        if hasattr(self, 'timeout'):
            self.timeout = 0.5
        elif sys.platform.startswith('java'):
            self.socket.settimeout(0.5)
        while not self._shutdown:
            try:
                self.handle_request()
            except (OSError, select.error) as err:
                if err.args[0] != errno.EINTR:
                    raise

    def stop(self):
        self._shutdown = True


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
        kw = getattr(self._library, name, None)
        return kw if is_function_or_method(kw) else None

    def get_keyword_arguments(self, name):
        kw = self._get_keyword(name)
        if not kw:
            return []
        return self._arguments_from_kw(kw)

    def _arguments_from_kw(self, kw):
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
        if name == '__init__' and inspect.ismodule(self._library):
            return ''
        keyword = self._get_keyword(name)
        doc = (inspect.getdoc(keyword) or '').lstrip()
        if getattr(keyword, 'robot_tags', []):
            tags = 'Tags: %s' % ', '.join(keyword.robot_tags)
            doc = '%s\n\n%s' % (doc, tags) if doc else tags
        return doc


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
        args, kwargs = self._handle_binary_args(args, kwargs or {})
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

    def _handle_binary_args(self, args, kwargs):
        args = [self._handle_binary_arg(a) for a in args]
        kwargs = dict((k, self._handle_binary_arg(v)) for k, v in kwargs.items())
        return args, kwargs

    def _handle_binary_arg(self, arg):
        return arg if not isinstance(arg, Binary) else arg.data


class StandardStreamInterceptor(object):

    def __init__(self):
        self.output = ''

    def __enter__(self):
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        return self

    def __exit__(self, *exc_info):
        stdout = sys.stdout.getvalue()
        stderr = sys.stderr.getvalue()
        close = [sys.stdout, sys.stderr]
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
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


if __name__ == '__main__':

    def stop(uri):
        server = test(uri, log_success=False)
        if server is not None:
            print('Stopping remote server at %s.' % uri)
            server.stop_remote_server()

    def test(uri, log_success=True):
        server = ServerProxy(uri)
        try:
            server.get_keyword_names()
        except:
            print('No remote server running at %s.' % uri)
            return None
        if log_success:
            print('Remote server running at %s.' % uri)
        return server

    def parse_args(args):
        actions = {'stop': stop, 'test': test}
        if not args or len(args) > 2 or args[0] not in actions:
            sys.exit('Usage:  python -m robotremoteserver test|stop [uri]')
        uri = args[1] if len(args) == 2 else 'http://127.0.0.1:8270'
        if '://' not in uri:
            uri = 'http://' + uri
        return actions[args[0]], uri

    action, uri = parse_args(sys.argv[1:])
    action(uri)
