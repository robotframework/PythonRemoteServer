from robot.api.deco import keyword

class Arguments(object):

    @keyword('Add ${quantity:\d+} Copies Of ${item} To Cart')
    def add_copies_to_cart(self, quantity, item):
        pass

    @keyword('')
    def embedded_name_empty(self):
        pass

    @keyword(tags=['tag1', 'tag2'])
    def login(username, password):
        '''
        This is keyword documentation'''
    
if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(Arguments(), '127.0.0.1', *sys.argv[1:])
