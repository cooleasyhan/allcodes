#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Supervisor listener
'''
import xmlrpclib
import logging
import socket
import time

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler)


class SupervisorRPC(object):

    '''SupervisorRPC'''

    def __init__(self, name, rpc_url):
        log.debug('[%s]init SupervisorRPC, url: %s', name, rpc_url)
        self.server = xmlrpclib.Server(rpc_url)
        self.server_name = name
        self.server_url = rpc_url
        self.state = None
        self.all_process_info = None
        self.refresh()

    def refresh(self):
        '''refresh'''
        self.state = self.server.supervisor.getState()
        self.all_process_info = self.server.supervisor.getAllProcessInfo()
        log.debug(
            '[%s]-----------refresh rst begin------------', self.server_name)
        log.debug(self.state)
        log.debug(self.all_process_info)
        log.debug(
            '[%s]-----------refresh rst end--------------', self.server_name)

    def stop_process(self, name):
        '''stop_process'''
        log.info('[%s]stop_process: %s', self.server_name, name)
        self.server.supervisor.stopProcess(name)
        self.refresh()

    def start_process(self, name):
        '''start_process'''
        log.info('[%s]start_process: %s', self.server_name, name)
        self.server.supervisor.startProcess(name)
        self.refresh()

    def is_alive(self):
        '''
        statecode   statename   Description
        2   FATAL   Supervisor has experienced a serious error.
        1   RUNNING Supervisor is working normally.
        0   RESTARTING  Supervisor is in the process of restarting.
        -1  SHUTDOWN    Supervisor is in the process of shutting down.
        '''
        cnt = 3
        while cnt >= 0:
            cnt -= 1
            self.refresh()
            state = self.state['statecode']
            if state == 1:
                return True
            if state == 2:
                return False

            if state in (0, -1):
                time.sleep(5)

        return False

    def get_process_info(self, name):
        '''
        {'name':           'process name',
         'group':          'group name',
         'start':          1200361776,
         'stop':           0,
         'now':            1200361812,
         'state':          1,
         'statename':      'RUNNING',
         'spawnerr':       '',
         'exitstatus':     0,
         'stdout_logfile': '/path/to/stdout-log',
         'stderr_logfile': '/path/to/stderr-log',
         'pid':            1}
        '''

        self.refresh()
        for prc in self.all_process_info:
            if prc['name'] == name:
                return prc

    def process_is_running(self, name):
        '''
        STOPPED (0)

        The process has been stopped due to a stop request or has never been started.
        STARTING (10)

        The process is starting due to a start request.
        RUNNING (20)

        The process is running.
        BACKOFF (30)

        The process entered the STARTING state but subsequently exited too quickly to move to the RUNNING state.
        STOPPING (40)

        The process is stopping due to a stop request.
        EXITED (100)

        The process exited from the RUNNING state (expectedly or unexpectedly).
        FATAL (200)

        The process could not be started successfully.
        UNKNOWN (1000)

        The process is in an unknown state (supervisord programming error).

        '''

        cnt = 3
        while cnt >= 0:
            cnt -= 1
            state = get_process_info(name)['state']

            if state == 10:
                return True
            if state in (0, 200):
                return False

            time.sleep(5)


class SupervisorListen(object):

    '''SupervisorListen'''

    def __init__(self, rpc_config):
        '''rpc_config['name']
           rpc_config['url']
        '''
        self.server_list = dict()
        for name, url in rpc_config:
            self.server_list[name] = SupervisorRPC(name, url)

    def send_alarm(self, warn_msg):
        '''send_alarm'''

    def linsten_alive(self):
        '''linsten_alive'''

        while True:
            warn_msg = ''
            for url, server in self.server_list:
                log.info('[%s]check alive %s', server.server_name, url)
                try:
                    if not server.is_alive():
                        warn_msg += 'url %s is down' % url
                except socket.error, socket_error:
                    log.exception(socket_error)
                    warn_msg += 'url %s is donw' % url
                except Exception, exc:
                    log.exception(exc)
                    warn_msg += 'url %s get unknow exception ' % url

            if warn_msg:
                log.warning('warn_msg: %s', warn_msg)
                self.send_alarm(warn_msg)
                time.sleep(120)

            time.sleep(10)

    def linsten_master_slave_process(self, master, slave, process):
        '''linsten_master_slave'''
        master_server = self.server_list[master]
        slave_server = self.server_list[slave]

        while True:
            # check master is alive, and the process is running

            master_state = master_server.process_is_running(process)
            slave_state = slave_server.process_is_running(process)

            if master_state and not slave_state:
                log.info('[%s-%s], %s is ok', master, slave, process)
            elif not master_state and slave_state:
                log.info(
                    '[%s-%s], %s is running in slave', master, slave, process)
            elif not master_state and not slave_state:
                log.warning(
                    '[%s-%s], %s is stoped in master and slave, \
                    try to start slave', master, slave, process)
                slave_server.start_process(process)
            else:
                log.warning(
                    '[%s-%s], %s is running in master and slave, \
                    try to stop slave', master, slave, process)
                slave_server.stop_process(process)

            time.sleep(10)
