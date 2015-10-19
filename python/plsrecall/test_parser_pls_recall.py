from parser_pls_recall import *


parser = PlsRecallParser()
a = file('PLSRecall.dat')
_list = parser.ParseFileObject(a)


for o in _list:
    print '--------'
    print o.time
    print o.sequence
    print o.username
    print o.database_name
    print o.query
    print '--------'
