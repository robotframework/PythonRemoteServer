class Dynamic(object):
    kws = {'passing': ['arg=None'],
           'failing': ['message'],
           'logging': ['message', 'level=INFO'],
           'returning': None,
           'kwargs': ['expected', '**kws']}

    def get_keyword_names(self):
        return list(self.kws)

    def run_keyword(self, name, args, kwargs=None):
        kw = globals()[name]
        return kw(*args, **(kwargs or {}))

    def get_keyword_arguments(self, name):
        return self.kws[name]


def passing(arg=None):
    assert not arg or '=' not in arg


def failing(message):
    raise AssertionError(message)


def logging(message, level='INFO'):
    print('*%s* %s' % (level, message))


def returning():
    return 'Hello, world!'


def kwargs(expected, **kws):
    actual = ', '.join('%s: %s' % (k, kws[k]) for k in sorted(kws))
    assert actual == expected


if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(Dynamic(), '127.0.0.1', *sys.argv[1:])

