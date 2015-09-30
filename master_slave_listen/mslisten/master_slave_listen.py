#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
master slave listen
'''
import xmlrpclib
import logging
import socket
import time


class MSListen(object):

    '''MSListen'''

    def __init__(self, master_rpc_url, slave_rpc_url, process_list):
        self.master_server = xmlrpclib.Server(master_rpc_url)
        self.slave_server = xmlrpclib.Server(slave_rpc_url)
        self.process_list = process_list

        self.status = dict()
        self.operation = dict()

    def get_status(self):
        '''through supervisor rpc, get the process status'''
        for process in self.process_list:
            state = dict()

            state['master'] = self.master_server.supervisor.getProcessInfo(
                process)['state']

            state['slave'] = self.slave_server.supervisor.getProcessInfo(
                process)['state']

            self.status[process] = state

    def stop_slave_process(self, process):
        '''stop_slave_process'''
        self.slave_server.supervisor.stopProcess(process)

    def start_slave_process(self, process):
        '''start_slave_process'''
        self.slave_server.supervisor.startProcess(process)

    def check_status(self):
        '''validate status'''
        self.operation = dict()

        for process, state in self.status:
            rst = ''
            if state['master'] == 20 and state['slave'] == 0:
                logging.info('%s: master is running', process)
                rst = 'DONOTHING'
            elif state['master'] == 0 and state['slave'] == 20:
                logging.warning('%s: slave is running', process)
                rst = 'ALARM'
            elif state['master'] == 20 and state['slave'] == 20:
                logging.warning('%s: master, slave is stoped', process)
                rst = 'STOP_SLAVE'
            elif state['master'] == 0 and state['slave'] == 0:
                logging.warning('%s: master, slave is stoped', process)
                rst = 'START_SLAVE'

            if rst not in('DONOTHING', 'ALARM'):
                self.operation[process] = rst

    def handler_operation(self):
        '''handler_operation'''
        for process, operation_code in self.operation:
            logging.info('handler process %s', process)

            if operation_code == 'STOP_SLAVE':
                logging.info('STOP_SLAVE')
                self.stop_slave_process(process)

            elif operation_code == 'START_SLAVE':
                logging.warning('START_SLAVE')
                self.start_slave_process(process)

    def send_alarm_sms(self):
        '''call sms interface to send out sms to admin'''

    def check_supervisor(self):

        try:
            slave_state = self.slave_server.supervisor.getState()
            master_state = self.master_server.supervisor.getState()

            if slave_state['statecode'] != 1 or master_state['statecode'] != 1:
                self.send_alarm_sms()
                return False

            return True
        except socket.error, _ex:
            logging.exception(_ex)
            return False
        except Exception, _ex:
            logging.exception(_ex)
            return False

    def heartbeat(self):
        '''heartbeat'''

        # self.get_status()
        # self.check_status()
        # if len(self.operation) == 0:
        #    return
        error_cnt = 0
        while True:
            rst = self.check_supervisor()
            if not rst:
                time.sleep(5)
                continue

            self.get_status()
            self.check_status()

            if len(self.operation) != 0:
                error_cnt += 1
            else:
                error_cnt = 0

            if error_cnt >= 3:
                break

            time.sleep(5)

        try:
            self.handler_operation()
        except Exception, _ex:
            logging.exception(_ex)
