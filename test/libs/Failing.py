import sys

if sys.version_info < (3,):
    import exceptions
else:
    import builtins as exceptions


class Failures(object):

    def failure(self, exception, message, evaluate=False):
        # TODO: Why try/except here?
        try:
            exception = globals()[exception]
        except KeyError:
            exception = getattr(exceptions, exception)
        if message is None:
            raise exception
        if evaluate:
            message = eval(message)
        if isinstance(message, tuple):
            raise exception(*message)
        raise exception(message)

    def failure_deeper(self, rounds=10):
        rounds = int(rounds)
        if rounds == 1:
            raise RuntimeError('Finally failing')
        self.failure_deeper(rounds-1)

    def continuable(self, message):
        self._raise_special(message, continuable=True)

    def fatal(self, message):
        self._raise_special(message, fatal='yes')

    def not_special(self, message):
        self._raise_special(message)

    def _raise_special(self, message, continuable=False, fatal=False):
        special = AssertionError(message)
        special.ROBOT_CONTINUE_ON_FAILURE = continuable
        special.ROBOT_EXIT_ON_FAILURE = fatal
        raise special


class MyException(Exception):
    pass


class SuppressNameException(Exception):
    ROBOT_SUPPRESS_NAME = True


if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(Failures(), '127.0.0.1', *sys.argv[1:])
