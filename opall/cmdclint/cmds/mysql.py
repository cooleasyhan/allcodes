#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''mysql command'''

from cmdclint.common.Command import BaseCommand
from cmdclint.api import get_env, update_env, MySQL


def validate_env(_paras):
    '''validate_env'''
    env_error_list = dict()
    for para in _paras:
        if not get_env(para):
            env_error_list[para] = '%s can not be null' % para
    return env_error_list


class Query(BaseCommand):

    '''Query'''
    _paras = ['mysql_user', 'mysql_password',
              'mysql_query_sql']

    def __init__(self, **kwargs):
        BaseCommand.__init__(self)
        if kwargs:
            self.set_env(kwargs)

    def set_env(self, kwargs):
        '''set_env'''
        if kwargs:
            update_env(kwargs)
        self.env_error_list = validate_env(self._paras)

    def execute(self):
        '''execute'''
        MySQL.query()

    def undo(self):
        '''undo'''
        pass


class CreateUser(BaseCommand):

    '''CreateUser'''
    _paras = ['mysql_user', 'mysql_password',
              'mysql_create_user_name',
              'mysql_create_user_password', 'mysql_host']

    def __init__(self, **kwargs):
        BaseCommand.__init__(self)

        if kwargs:
            update_env(kwargs)
        self.env_error_list = validate_env(self._paras)

    def execute(self):
        '''execute'''
        MySQL.create_user()

    def undo(self):
        '''undo'''
        raise NotImplementedError
