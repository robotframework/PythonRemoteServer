class FirstLib:
    def keyword_from_first_library(self):
        pass

class SecondLib:
    def keyword_from_second_library(self):
        pass

class ThirdLib:
    def keyword_from_third_library(self):
        pass

if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer([FirstLib(), SecondLib(), ThirdLib()], '127.0.0.1', *sys.argv[1:])
