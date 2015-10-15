from mslisten import SupervisorListen, SupervisorRPC
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s]%(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')


def testalive():
    sms01 = SupervisorRPC(
        'localhost', 'http://admin:qihoo360@10.142.103.191:9001/RPC2')
    sms02 = SupervisorRPC(
        'localhost', 'http://admin:qihoo360@106.38.193.174:9001/RPC2')
    sms03 = SupervisorRPC(
        'localhost', 'http://admin:qihoo360@10.138.70.140:9001/RPC2')
    super_listen = SupervisorListen()
    super_listen.add_supervisor(super1)

    super_listen.linsten_alive()


def testmaster():
    super_listen = SupervisorListen()
    super1 = SupervisorRPC(
        'localhost', 'http://admin:qihoo360@127.0.0.1:9001/RPC2')


    super2 = SupervisorRPC(
        'localhost2', 'http://admin:qihoo360@127.0.0.1:9001/RPC2')

    super_listen.add_supervisor(super1)
    super_listen.add_supervisor(super2)

    super_listen.linsten_master_slave_process('localhost', 'localhost2', 'test1')

testalive()
