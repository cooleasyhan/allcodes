#!/usr/bin/env python
# coding=utf-8

# -*- coding: UTF-8 -*-

import sys


sys.path.append("..")

import traceback
import logging
from smslib.mq import MQConsumer
from smslib.sms import Message, Channel
from smslib.mq import RptPorducer, RetryPorducer
reload(sys)
sys.setdefaultencoding("utf-8")


class SmsConsumerRstProducer(object):
    def __init__(self):

        self.rptP = RptPorducer()
        self.retryP = RetryPorducer()

    def send_to_rpt_mq(self, smsList):
        self.rptP.sendSms(smsList)

    def send_to_retry_mq(self, smsList):
        self.retryP.sendSms(smsList)

class SmsConsumerBase(SmsConsumerRstProducer):

    def __init__(self, mq_type):
        SmsConsumerRstProducer.__init__(self)
        self.mq_type = mq_type
        self.consumer = MQConsumer(mq_type)

    def get_messages(self, cnt=1):

        jsonList = self.consumer.nextMessages(cnt)
        smsList = list()
        for jsonStr in jsonList:
            try:
                m = Message()
                m.readJson(jsonStr)
                smsList.append(m)
            except Exception, e:
                logging.exception('error to transfer mq message to sms object, mq message: %s' %(jsonStr))

        return smsList


    def handle_messages(self, smsList):
        raise NotImplementedError

