'''
BaseCommand
'''


class BaseCommand(object):

    '''BaseCommand'''

    def __init__(self):
        pass

    def execute(self):
        '''execute'''
        raise NotImplementedError

    def undo(self):
        '''undo'''
        raise NotImplementedError
