class Hybrid(object):

    def get_keyword_names(self):
        return ['passing', 'failing', 'logging', 'returning', 'kwargs']

    def __getattr__(self, name):
        try:
            return globals()[name]
        except KeyError:
            raise AttributeError(name)


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

    RobotRemoteServer(Hybrid(), '127.0.0.1', *sys.argv[1:])

