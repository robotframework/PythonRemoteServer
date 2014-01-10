class MyObject:

    def __init__(self, name='<MyObject>'):
        self.name = name

    def __str__(self):
        return self.name


BYTE_STRING = 'Hello, world!'
UNICODE_STRING = (u'Hyv\u00E4\u00E4 y\u00F6t\u00E4. '
                  u'\u0421\u043F\u0430\u0441\u0438\u0431\u043E!')
CONTROL_CHAR = '\x01'

LIST = ['One', -2, False]
EMPTY_LIST = []
LIST_WITH_NONE = [None]
LIST_WITH_OBJECTS = [MyObject(1), MyObject(2)]
NESTED_LIST = [[True, False], [[1, None, MyObject(), {}]]]

TUPLE = ('One', -2, False)
EMPTY_TUPLE = ()
NESTED_TUPLE = ((True, False), [(1, None, MyObject(), {})])

DICT = {'one': 1, 'spam': 'eggs'}
EMPTY_DICT = {}
DICT_WITH_NON_STRING_KEYS = {1: 2, None: True}
DICT_WITH_NONE = {'As value': None, None: 'As key'}
DICT_WITH_OBJECTS = {'As value': MyObject(1), MyObject(2): 'As key'}
NESTED_DICT = {1: {None: False},
               2: {'A': {'n': None},
                   'B': {'o': MyObject(), 'e': {}}}}

REPLACEMENT_CHARACTER = u'\uFFFD'
