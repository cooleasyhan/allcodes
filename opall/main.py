
m = __import__('cmds')


def query():
    mysql_query = getattr(m, 'mysql_query')

    q = mysql_query(host_string='localhost',
                    mysql_user='root', mysql_password='root',
                    mysql_query_sql='select * from mysql.user')
    print q.env
    q.execute()


def run(conf):
    _module = __import__(conf["module"])
    _class = getattr(_module, conf["command"])
    obj = _class()
    obj.set_env(conf['args'])
    print obj.env

    print obj.env_error_list

    obj.execute()


if __name__ == '__main__':

    conf = {"function_name": "test", "command": "mysql_query",
            "module": "cmds",
            "args": {"host_string": "localhost", "password": "yihan", "mysql_user": "root", "mysql_password": "root", "mysql_query_sql": "select * from mysql.user"}}

    run(conf)
