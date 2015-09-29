#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''Api'''

from fabric.api import env
from mysql import MySQL


def set_env(key, value):
    '''set_env'''
    env[key] = value


def get_env(key):
    '''get_env'''
    return env[key]


def update_env(_dict):
    '''update_env'''
    env.update(_dict)


__all__ = ['set_env', 'get_env', 'update_env', 'MySQL', 'env']
