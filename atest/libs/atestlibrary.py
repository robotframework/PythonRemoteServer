import sys


class AcceptanceTestLibrary:
    _unicode = (u'Hyv\u00E4\u00E4 y\u00F6t\u00E4. '
                u'\u0421\u043F\u0430\u0441\u0438\u0431\u043E!')

    def get_server_language(self):
        return 'Jython' if sys.platform.startswith('java') else 'Python'

    # Return values

    def return_string(self):
        return 'Hello, world!'

    def return_unicode_string(self):
        return self._unicode

    def return_empty_string(self):
        return ''

    def return_control_char(self):
        return '\x01'

    def return_integer(self):
        return 42

    def return_negative_integer(self):
        return -1

    def return_float(self):
        return 3.14

    def return_negative_float(self):
        return -0.5

    def return_zero(self):
        return 0

    def return_boolean_true(self):
        return True

    def return_boolean_false(self):
        return False

    def return_nothing(self):
        pass

    def return_object(self):
        return MyObject()

    def return_list(self):
        return ['One', -2, False]

    def return_empty_list(self):
        return []

    def return_list_containing_none(self):
        return [None]

    def return_list_containing_objects(self):
        return [MyObject(1), MyObject(2)]

    def return_nested_list(self):
        return [[True, False], [[1, None, MyObject(), {}]]]

    def return_tuple(self):
        return ('One', -2, False)

    def return_empty_tuple(self):
        return ()

    def return_nested_tuple(self):
        return ((True, False), [(1, None, MyObject(), {})])

    def return_dictionary(self):
        return {'one': 1, 'spam': 'eggs'}

    def return_empty_dictionary(self):
        return {}

    def return_dictionary_with_non_string_keys(self):
        return {1: 2, None: True}

    def return_dictionary_containing_none(self):
        return {'As value': None, None: 'As key'}

    def return_dictionary_containing_objects(self):
        return {'As value': MyObject(1), MyObject(2): 'As key'}

    def return_nested_dictionary(self):
        return {1: {None: False},
                2: {'A': {'n': None}, 'B': {'o': MyObject(), 'e': {}}}}


class MyObject:
    def __init__(self, index=''):
        self.index = index
    def __str__(self):
        return '<MyObject%s>' % self.index


if __name__ == '__main__':
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(AcceptanceTestLibrary(), '127.0.0.1', *sys.argv[1:])
