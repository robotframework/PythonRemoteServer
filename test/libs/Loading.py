import sys
from robot.api.deco import keyword
from robotremoteserver import RobotRemoteServer

class KwLibrary:
    def basic(self):
        pass

    @keyword('Complex', tags=['tag1', 'tag2'])
    def complex_kw(self, arg1, *, named, namedWithDefault='something', **kwargs):
        pass

class OneByOneRemoteServer(RobotRemoteServer):

    def _register_functions(self, server):
        """
        Do not register get_library_information. This removes the bulk load feature
        and checks the fallback to loading individual keywords.
        """
        server.register_function(self.get_keyword_names)
        server.register_function(self.run_keyword)
        server.register_function(self.get_keyword_arguments)
        server.register_function(self.get_keyword_documentation)
        server.register_function(self.get_keyword_tags)
        server.register_function(self.get_keyword_types)
        server.register_function(self.stop_remote_server)

class BulkLoadRemoteServer(RobotRemoteServer):

    def _register_functions(self, server):
        """
        Individual get_keyword_* methods are not registered.
        This removes the fall back scenario should get_library_information fail.
        """
        server.register_function(self.get_library_information)
        server.register_function(self.run_keyword)
        server.register_function(self.stop_remote_server)

if __name__ == '__main__':
    if 'BulkMode' in sys.argv:
        BulkLoadRemoteServer(KwLibrary(), '127.0.0.1', *sys.argv[1:])
    elif 'SingleMode' in sys.argv:
        OneByOneRemoteServer(KwLibrary(), '127.0.0.1', *sys.argv[1:])
    else:
        raise ValueError("Pass either BulkMode or SingleMode to run this library")
