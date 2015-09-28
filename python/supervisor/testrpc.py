import supervisor.xmlrpc
import xmlrpclib

#p = xmlrpclib.ServerProxy('http://127.0.0.1',
#        transport=supervisor.xmlrpc.SupervisorTransport(
#            None, None,
#            'unix:///tmp/supervisor.sock'))

#print p.supervisor.getState()

import supervisor.xmlrpc
import xmlrpclib
import xmlrpclib


import time


def get_status(server, process_name):
    try:
        return server.supervisor.getProcessInfo(process_name)['state']
    except Exception:
        return -1


server = xmlrpclib.Server(
            'http://admin:admin@192.168.175.130:9001/RPC2')



print 'aaaa'
#methods = server.system.listMethods()
# print methods
while True:

    state = get_status(server, "test")
    if state == 20:
        print 'it is running'
    else:
        print 'warning it is stoped'
    time.sleep(5)

