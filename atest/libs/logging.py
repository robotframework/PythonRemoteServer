class Logging(object):

    def logging(self, message, level='', evaluate=False):
        if evaluate:
            message = eval(message)
        if level:
            message = '*%s* %s' % (level, message)
        print message

    def multiple_messages_with_different_levels(self):
        print 'Info message'
        print '*DEBUG* Debug message'
        print '*INFO* Second info'
        print 'this time with two lines'
        print '*INFO* Third info'
        print '*TRACE* This is ignored'
        print '*WARN* Warning'

    def logging_and_failing(self):
        print '*INFO* This keyword will fail!'
        print '*WARN* Run for your lives!!'
        raise AssertionError('Too slow')

    def logging_and_returning(self, logged, returned):
        print logged
        return returned


if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(Logging(), '127.0.0.1', *sys.argv[1:])
