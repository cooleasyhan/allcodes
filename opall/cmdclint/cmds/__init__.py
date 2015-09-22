'''
Command Package, all new command should be placed in here
'''
from cmdclint.cmds.mysql import Query as MysqlQuery
from cmdclint.cmds.mysql import CreateUser as MysqlCreateUser


__all__ = ['MysqlQuery', 'MysqlCreateUser']
