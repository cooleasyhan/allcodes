
m = __import__('cmds')


def query():
    mysql_query = getattr(m, 'mysql_query')

    q = mysql_query('root', 'root', 'select * from mysql.user')
    q.execute()
