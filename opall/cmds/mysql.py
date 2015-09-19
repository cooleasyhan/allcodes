import sys
sys.path.append("..")
from common.Command import BaseCommand
from api import set_env, update_env, mysql


class Query(BaseCommand):

    '''Query'''

    def __init__(self, user, password, sql, **kwargs):
        BaseCommand.__init__(self)
        self.user = user
        self.password = password
        self.sql = sql
        self.init_env()
        if kwargs:
            update_env(kwargs)

    def init_env(self):
        '''init_env'''
        set_env('mysql_user', self.user)
        set_env('mysql_password', self.password)
        set_env('mysql_query_sql', self.sql)

    def execute(self):
        '''execute'''
        mysql.query()

    def undo(self):
        '''undo'''
        pass


class CreateUser(BaseCommand):

    '''CreateUser'''

    def __init__(self, user, password,
                 new_user_name, new_user_pwd, new_user_host='localhost', **kwargs):
        BaseCommand.__init__(self)
        self.user = user
        self.password = password
        self.new_user_name = new_user_name
        self.new_user_pwd = new_user_pwd
        self.new_user_host = new_user_host
        self.init_env()
        if kwargs:
            update_env(kwargs)

    def init_env(self):
        '''init_env'''
        set_env('mysql_user', self.user)
        set_env('mysql_password', self.password)
        set_env('mysql_create_user_name', self.new_user_name)
        set_env('mysql_create_user_password', self.new_user_pwd)
        set_env('mysql_host', self.new_user_host)

    def execute(self):
        '''execute'''
        mysql.create_user()

    def undo(self):
        '''undo'''
        raise NotImplementedError
