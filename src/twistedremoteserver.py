#  Copyright (C) 2014 David Arnold
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

import os
import sys
from twisted.web import server
from twisted.web.xmlrpc import XMLRPC, NoSuchFunction
from twisted.internet import reactor, defer
from robotremoteserver import RobotRemoteInterface


class TwistedRemoteServer(XMLRPC):
    """A Robot Framework Remote Server using the Twisted event loop.

    This is useful if you have other network functionality to be exposed by
    the remote server, using Twisted, and want to offer both the RF XML-RPC
    interface and the other interface from the one process.
    """
    
    def __init__(self, library, host='127.0.0.1', port=8270, port_file=None,
                 allow_stop=True):
        """Configure remote Twisted-based server.

        :param: library:    Test library instance or module to host.
        :param: host:
        """

        self.server_address = (host, port)
        self._funcs = {}
        self._robot = RobotRemoteInterface(library, self)
        reactor.listenTCP(int(port), server.Site(self._robot), interface=host)
        return

    def register_function(self, func, name=None):
        """Register a function to be exposed via XML-RPC.

        This method is used by the RobotRemoteInterface to register its
        public functions."""

        if not name:
            name = func.__name__
        self._funcs[name] = func
        return

    def stop_remote_server(self):
        """Stop the server, if this is allowed.

        This method is used by the RobotRemoteInterface to permit remote
        clients to shut down the server.  See :allow_stop: in the
        constructor for a way to prevent this."""

        prefix = 'Robot Framework remote server at %s:%s ' % self.server_address
        if self._allow_stop:
            self._log(prefix + 'stopping.')
            reactor.callLater(1, reactor.stop)

        else:
            self._log(prefix + 'does not allow stopping.', 'WARN')
        return self._shutdown

    def lookupProcedure(self, path):
        """Lookup callable for XML-RPC request.

        This method is overridden from XMLRPC."""

        try:
            return self._funcs[path]
        except KeyError:
            raise NoSuchFunction(self.NOT_FOUND, "No such function: %s" % path)

    def listProcedures(self):
        """Return a list of the valid XML-RPC requests.

        This method is overriden from XMLRPC."""

        return self._funcs.keys()

    def serve_forever(self):
        """Start remote server responding to client connections."""
        print 'Robot Framework remote server starting at %s:%s' % \
              self.server_address
        sys.stdout.flush()
        reactor.run()
        return


if __name__ == "__main__":
    class Library(object):
        def count_items_in_directory(self, path):
            """Returns the number of items in directory `path`."""
            return len([i for i in os.listdir(path) if not i.startswith('.')])

    server = TwistedRemoteServer(Library())
    server.serve_forever()
