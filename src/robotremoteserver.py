#  Copyright 2008-2012 Nokia Siemens Networks Oyj
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

import sys
import inspect
import traceback
from StringIO import StringIO
from SimpleXMLRPCServer import SimpleXMLRPCServer
try:
    import signal
except ImportError:
    signal = None


__version__ = 'devel'


class RobotRemoteServer(SimpleXMLRPCServer):
    allow_reuse_address = True
    _generic_exceptions = (AssertionError, RuntimeError, Exception)
    _fatal_exceptions = (SystemExit, KeyboardInterrupt)

    def __init__(self, library, host='localhost', port=8270, allow_stop=True):
        SimpleXMLRPCServer.__init__(self, (host, int(port)), logRequests=False)
        self._library = library
        self._is_dynamic = self._get_routine('run_keyword') and \
                           self._get_routine('get_keyword_names')
        self._allow_stop = allow_stop
        self._register_functions()
        self._register_signal_handlers()
        self._log('Robot Framework remote server starting at %s:%s' % (host, port))
        self.serve_forever()

    def _register_functions(self):
        self.register_function(self.get_keyword_names)
        self.register_function(self.run_keyword)
        if not self._is_dynamic or \
                (self._is_dynamic and self._get_routine('get_keyword_arguments')):
            self.register_function(self.get_keyword_arguments)
        if not self._is_dynamic or \
                (self._is_dynamic and self._get_routine('get_keyword_documentation')):
            self.register_function(self.get_keyword_documentation)
        self.register_function(self.stop_remote_server)

    def _register_signal_handlers(self):
        def stop_with_signal(signum, frame):
            self._allow_stop = True
            self.stop_remote_server()
        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, stop_with_signal)
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, stop_with_signal)

    def serve_forever(self):
        self._shutdown = False
        while not self._shutdown:
            self.handle_request()

    def stop_remote_server(self):
        prefix = 'Robot Framework remote server at %s:%s ' % self.server_address
        if self._allow_stop:
            self._log(prefix + 'stopping')
            self._shutdown = True
        else:
            self._log(prefix + 'does not allow stopping', 'WARN')
        return True

    def get_keyword_names(self):
        get_kw_names = self._get_routine('get_keyword_names')
        if get_kw_names is None:
            names = [attr for attr in dir(self._library) if attr[0] != '_'
                     and inspect.isroutine(getattr(self._library, attr))]
        else:
            names = get_kw_names()
        return names + ['stop_remote_server']

    def run_keyword(self, name, args):
        result = {'error': '', 'traceback': '', 'return': ''}
        self._intercept_stdout()
        try:
            if name == 'stop_remote_server':
                return_value = self.stop_remote_server()
            elif self._is_dynamic:
                return_value = self._get_routine('run_keyword')(name, args)
            else:
                return_value = self._get_keyword(name)(*args)
        except:
            result['status'] = 'FAIL'
            result['error'], result['traceback'] = self._get_error_details()
        else:
            result['status'] = 'PASS'
            result['return'] = self._handle_return_value(return_value)
        result['output'] = self._restore_stdout()
        return result

    def get_keyword_arguments(self, name):
        if name == 'stop_remote_server':
            return []
        elif self._is_dynamic:
            return list(self._get_routine('get_keyword_arguments')(name))
        else:
            kw = self._get_keyword(name)
            if not kw:
                return []
            return self._arguments_from_kw(kw)

    def _get_routine(self, name):
        rnames = {
            'run_keyword':
                ['run_keyword', 'runKeyword'],
            'get_keyword_names':
                ['get_keyword_names', 'getKeywordNames'],
            'get_keyword_arguments':
                ['get_keyword_arguments', 'getKeywordArguments'],
            'get_keyword_documentation':
                ['get_keyword_documentation', 'getKeywordDocumentation']}
        for rname in rnames[name]:
            rt = getattr(self._library, rname, None)
            if inspect.isroutine(rt):
                return rt
        return None

    def _arguments_from_kw(self, kw):
        args, varargs, _, defaults = inspect.getargspec(kw)
        if inspect.ismethod(kw):
            args = args[1:]  # drop 'self'
        if defaults:
            args, names = args[:-len(defaults)], args[-len(defaults):]
            args += ['%s=%s' % (n, d) for n, d in zip(names, defaults)]
        if varargs:
            args.append('*%s' % varargs)
        return args

    def get_keyword_documentation(self, name):
        if name == 'stop_remote_server':
            return 'Stops the remote server.\n\n' + \
                   'The server may be configured so that users cannot stop it.'
        get_kw_doc = self._get_routine('get_keyword_documentation')
        if self._is_dynamic and get_kw_doc:
            return get_kw_doc(name)
        if name == '__intro__':
            return inspect.getdoc(self._library) or ''
        if name == '__init__' and inspect.ismodule(self._library):
            return ''
        return inspect.getdoc(self._get_keyword(name)) or ''

    def _get_keyword(self, name):
        kw = getattr(self._library, name, None)
        if inspect.isroutine(kw):
            return kw
        return None

    def _get_error_details(self):
        exc_type, exc_value, exc_tb = sys.exc_info()
        if exc_type in self._fatal_exceptions:
            self._restore_stdout()
            raise
        return (self._get_error_message(exc_type, exc_value),
                self._get_error_traceback(exc_tb))

    def _get_error_message(self, exc_type, exc_value):
        name = exc_type.__name__
        message = self._get_message_from_exception(exc_value)
        if not message:
            return name
        if exc_type in self._generic_exceptions:
            return message
        return '%s: %s' % (name, message)

    def _get_message_from_exception(self, value):
        # UnicodeError occurs below 2.6 and if message contains non-ASCII bytes
        try:
            return unicode(value)
        except UnicodeError:
            return ' '.join([unicode(a, errors='replace') for a in value.args])

    def _get_error_traceback(self, exc_tb):
        # Latest entry originates from this class so it can be removed
        entries = traceback.extract_tb(exc_tb)[1:]
        trace = ''.join(traceback.format_list(entries))
        return 'Traceback (most recent call last):\n' + trace

    def _handle_return_value(self, ret):
        if isinstance(ret, (basestring, int, long, float)):
            return ret
        if isinstance(ret, (tuple, list)):
            return [self._handle_return_value(item) for item in ret]
        if isinstance(ret, dict):
            return dict([(self._str(key), self._handle_return_value(value))
                         for key, value in ret.items()])
        return self._str(ret)

    def _str(self, item):
        if item is None:
            return ''
        return str(item)

    def _intercept_stdout(self):
        # TODO: What about stderr?
        sys.stdout = StringIO()

    def _restore_stdout(self):
        output = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        return output

    def _log(self, msg, level=None):
        if level:
            msg = '*%s* %s' % (level.upper(), msg)
        print msg
