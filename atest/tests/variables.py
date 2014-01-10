class MyObject(object):

    def __init__(self, name='<MyObject>'):
        self.name = name

    def __str__(self):
        return self.name
