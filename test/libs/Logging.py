from __future__ import print_function

import sys


class Logging(object):

    def logging(self, message, level='', evaluate=False, stderr=False):
        if evaluate and evaluate != 'False':
            message = eval(message)
        if level:
            message = '*%s* %s' % (level, message)
        stream = sys.stdout if not stderr else sys.stderr
        print(message, file=stream)

    def multiple_messages_with_different_levels(self):
        print('Info message')
        print('*DEBUG* Debug message')
        print('*INFO* Second info')
        print('this time with two lines')
        print('*INFO* Third info')
        print('*TRACE* This is ignored')
        print('*WARN* Warning')

    def logging_and_failing(self):
        print('*INFO* This keyword will fail!')
        print('*WARN* Run for your lives!!')
        raise AssertionError('Too slow')

    def logging_and_returning(self, logged, returned):
        print(logged)
        return returned

    def logging_both_to_stdout_and_stderr(self, *messages):
        for index, msg in enumerate(messages):
            stream = sys.stdout if index % 2 == 0 else sys.stderr
            stream.write(msg)

if __name__ == '__main__':
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(Logging(), '127.0.0.1', *sys.argv[1:])
