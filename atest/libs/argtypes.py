class ArgumentTypes(object):

    def argument_should_be_correct(self, argument, expected):
        expected = eval(expected)
        if argument != expected:
            raise AssertionError('%r != %r' % (argument, expected))


if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(ArgumentTypes(), '127.0.0.1', *sys.argv[1:])
