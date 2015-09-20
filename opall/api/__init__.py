from fabric.api import env
from mysql import MySQL as mysql


def set_env(key, value):
    '''set_env'''
    env[key] = value


def get_env(key):
    '''get_env'''
    return env[key]


def update_env(_dict):
    '''update_env'''
    env.update(_dict)


__all__ = ['set_env', 'get_env', 'mysql', 'env']
