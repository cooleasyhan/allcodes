import fabtools
from fabric.api import env


class MySQL(object):

    '''
    env['mysql_user'] = 'root'
    env['mysql_password'] = 'root'

    env['mysql_host'] = '127.0.0.1'
    env['mysql_query_sql'] = 'select count(1) from mysql.user'
    env['mysql_create_user_name'] = 'yihan'
    env['mysql_create_user_password'] = 'yihan123'
    '''

    @staticmethod
    def create_user():
        '''Create DB user if it does not exist'''

        if not fabtools.mysql.user_exists(env.get('mysql_create_user_name')):
            fabtools.mysql.create_user(env.get('mysql_create_user_name'),
                                       password=env.get('mysql_create_user_password'))

    @staticmethod
    def query():
        '''
        Run a MySQL query.
        '''
        print env
        fabtools.mysql.query(env.get('mysql_query_sql'))
