import exceptions


class Failures(object):

    def failure(self, exception, message, evaluate=False):
        try:
            exception = globals()[exception]
        except KeyError:
            exception = getattr(exceptions, exception)
        if message is None:
            raise exception
        if evaluate:
            message = eval(message)
        raise exception(message)

    def failure_deeper(self, rounds=10):
        rounds = int(rounds)
        if rounds == 1:
            raise RuntimeError('Finally failing')
        self.failure_deeper(rounds-1)


class MyException(Exception):
    pass


if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(Failures(), '127.0.0.1', *sys.argv[1:])
