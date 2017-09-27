import os


"""Testing basic communication and keyword documentation using module.

Same stuff as in Basics.py but this library is implemented as a module,
not as a class.
"""


def passing():
    """This keyword passes.

    See `Failing`, `Logging`, and `Returning` for other basic keywords.
    """
    pass


def get_pid():
    """Return process id of the server that is serving this library."""
    return os.getpid()


def failing(message):
    """This keyword fails with provided `message`"""
    raise AssertionError(message)


def logging(message, level='INFO'):
    """This keywords logs given `message` with given `level`

    Example:
    | Logging | Hello, world! |      |
    | Logging | Warning!!!    | WARN |
    """
    print('*%s* %s' % (level, message))


def returning(value):
    """This keyword returns the given `value`."""
    return value


def _private_method():
    """This is not a keyword. Nor is the next one."""
    pass


def __private_method():
    pass


ATTRIBUTE = 'Not a keyword'


if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    if sys.argv[-1] == 'no_stop':
        conf = {'allow_remote_stop': False}
        sys.argv.pop()
    else:
        conf = {}
    library = sys.modules[__name__]
    RobotRemoteServer(library, '127.0.0.1', *sys.argv[1:], **conf)
