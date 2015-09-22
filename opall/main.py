import importlib
m = __import__('cmdclint.cmds')

from cmdclint import CmdClint


def query():
    MySQL = getattr(m, 'MySQL')

    q = MySQL(host_string='localhost',
              mysql_user='root', mysql_password='root',
              mysql_query_sql='select * from mysql.user')
    print q.env
    q.execute()


def run(conf):

    conf = {"function_name": "test", "command": "MysqlQuery",
            "module": "cmdclint.cmds",
            "args": {"host_string": "localhost", "password": "yihan", "mysql_user": "root", "mysql_password": "root", "mysql_query_sql": "select * from mysql.user"}}

    _module = importlib.import_module(conf["module"])
    _class = getattr(_module, conf["command"])
    obj = _class()
    obj.set_env(conf['args'])
    print obj.env

    print obj.env_error_list

    obj.execute()


if __name__ == '__main__':
    cmd_clint = CmdClint()
    cmd_clint.server_forever()
