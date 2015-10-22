#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
import time
import logging

from pyqbus import PyConsumer4Storm
from pyqbus import PyProducer

import mq_setting as mq_cfg


class MQConsumer(object):

    '''MessageQueue'''

    def __init__(self, type):
        logging.info('MQConsumer Init')
        if mq_cfg.mqs.has_key(type):
            self._mqconf = mq_cfg.mqs[type]
            logging.info('mq config : %s' % self._mqconf)
        else:
            raise Exception(
                'messageQueue setting error', 'no setting for type: %s' % type)
        try:
            self._consumer = PyConsumer4Storm(self._mqconf['zk_cluster'], self._mqconf['topic'],
                                          self._mqconf['group'], self._mqconf['conf_path'])
            logging.info('MQConsumer Init success')
        except:
            logging.exception("MQConsumer Init Error")

    def nextMessages(self, cnt=1):

        result = list()
        try:
            while len(result) < cnt:
                temp_result = self._consumer.nextMessages()
                logging.info('!****!%s!****!' %temp_result)
                ret = self._consumer.commitOffset()
                count = len(temp_result)
                if ret == 1:
                    logging.info(
                        "Get messages success, msg cnts: %d  commitOffset rst: %d" % (count, ret))
                else:
                    logging.warning(
                        "Get messages success, msg cnts: %d  commitOffset rst error: %d" % (count, ret))
                if count == 0:
                    break
                else:
                    result += temp_result
            return result
        except:
            logging.excetion("MQConsumer nextMessage Error")
            return result



class MQProducer(object):

    '''MessageQueue Producer'''

    def __init__(self, type):
        logging.info('MQProducer Init')
        if mq_cfg.mqs.has_key(type):
            self._mqconf = mq_cfg.mqs[type]
            logging.info('mq config : %s' % self._mqconf)
        else:
            raise Exception(
                'messageQueue setting error', 'no setting for type: %s' % type)

        try:
            self._producer = PyProducer(self._mqconf[
                                    'zk_cluster'], self._mqconf['conf_path'])  # self._mqconf['conf_path'])
            logging.info('MQProducer Init success')
        except:
            logging.exception("MQProducer Init Error")

    def send(self, messages):
        try:
            errstr = ""
            ret = self._producer.send(messages, self._mqconf['topic'], errstr)
            if (ret == 0):
                logging.warning("sent to mq failed, mq: %s messages: %s, error str: %s" % (self._mqconf, messages, errstr))
                return False
            return True
        except:
            logging.exception("sent to mq failed2, mq: %s messages: %s, error str: %s" % (self._mqconf, messages, errstr))

        
    def sendSms(self, smsList):
        mq_msgs = list()
        for sms in smsList:
            mq_msgs.append(sms.toJsonStr())
        return self.send(mq_msgs)


class RptPorducer(MQProducer):
    def __init__(self, type = 'rpt_mq'):
        MQProducer.__init__(self, type)


class RetryPorducer(MQProducer):
    def __init__(self, type = 'retry_mq'):
        MQProducer.__init__(self, type)




def main():
    '''main
    '''
    mp = MQProducer('unicom_mq')
    mc = MQConsumer('unicom_mq')
    msg = []
    msg.append('abc')
    msg.append('sdfsd')
    for i in range(1):
        pass
        ret = mp.send(msg)
        print ret
        rst = mc.nextMessages()
        print rst


if __name__ == '__main__':
    import logging
    print 'a'
    logging.basicConfig(level=logging.DEBUG)
    main()
