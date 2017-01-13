from robot.api.deco import keyword


class KeywordDecorator(object):

    @keyword('Custom name')
    def _this_name_doesnt_matter(self, arg):
        assert arg == 'arg'

    @keyword('Result of ${expression} should be ${result:\d+}')
    def calculate(self, expression, expected):
        assert eval(expression) == int(expected)

    @keyword
    def just_marker(self):
        pass

    @keyword(tags=['tag1', 'tag2'])
    def tags(self):
        pass

    @keyword('Tags with doc (and custom name)', ['tag1'])
    def tags_(self):
        """Keyword documentation."""


if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(KeywordDecorator(), '127.0.0.1', *sys.argv[1:])
