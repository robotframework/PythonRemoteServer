import sys

if sys.version_info < (3,):
    from collections import Mapping
else:
    from collections.abc import Mapping


class Returning(object):

    def return_evaluated(self, value):
        return eval(value)


class MyObject(object):

    def __init__(self, name='<MyObject>'):
        self.name = name

    def __str__(self):
        return self.name


class MyMapping(Mapping):

    def __init__(self, data=None, **extra):
        self.data = dict(data or {}, **extra)

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(Returning(), '127.0.0.1', *sys.argv[1:])
