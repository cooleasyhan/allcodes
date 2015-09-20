'''
BaseCommand
'''
import sys
sys.path.append("..")
from api import env


class BaseCommand(object):

    '''BaseCommand'''

    def __init__(self):
        self.env = env

    def execute(self):
        '''execute'''
        raise NotImplementedError

    def undo(self):
        '''undo'''
        raise NotImplementedError
