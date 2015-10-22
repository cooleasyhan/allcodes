#!/usr/bin/env python
# coding=utf-8

# -*- coding: UTF-8 -*-
import json
import time


class M(type):

    def __new__(cls, name, bases, classdict):
        for attr in classdict.get('__slots__', ()):
            def getter(self, attr=attr):
                return getattr(self, attr)

            def setter(self, val=0, attr=attr):
                return setattr(self, attr, val)
            classdict['get' + attr] = getter
            classdict['set' + attr] = setter
        return type.__new__(cls, name, bases, classdict)


class Message(object):
    __metaclass__ = M
    __slots__ = ['Id', 'Mobile', 'Msg', 'CreationDate', 'LastUpdateDate', 'Status',
                 'SendId', 'PhoneType', 'IsVerify', 'Method', 'Language', 'SqlTable', 'Channel', 'SpMsgId', 'Template']

    FETCHED_STATUS = 21
    SENDED_TO_GATAWAY = 1
    SENDED_TO_GATAWAY_ERROR = 2
    ABNORMAL_STATUS = 3
    SENDED_TO_USER = 23

    def __init__(self):
        self.setId(None)
        self.setMsg(None)
        self.setCreationDate(None)
        self.setLastUpdateDate(None)
        self.setStatus(None)
        self.setMobile(None)
        self.setPhoneType(None)
        self.setIsVerify(None)
        self.setMethod(None)
        self.setLanguage(None)
        self.setSqlTable(None)
        self.setChannel(None)
        self.setSendId(None)
        self.setSpMsgId(None)
        #add template
        self.setTemplate(None)

    # sync with db table sms0506
    # id, msg, app_id, date_format(insert_time,'%s') insert_time, mobile,
    # phone_type,is_verify, method, language
    def setValuesFromDB(self, _dict):
        self.setId(_dict['id'])
        self.setMsg(_dict['msg'])
        self.setCreationDate(_dict['insert_time'])
        self.setMobile(_dict['mobile'])
        self.setPhoneType(_dict['phone_type'])
        self.setIsVerify(_dict['is_verify'])
        self.setMethod(_dict['method'])
        self.setLanguage(_dict['language'])
        self.setSqlTable(_dict['sql_table'])
        #add template
        self.setTemplate(_dict['template'])

    def toDict(self):
        tmpDict = dict()
        for attr in Message.__slots__:
            tmpDict[attr] = getattr(self, attr)
        return tmpDict

    def readDict(self, _dict):
        for attr in Message.__slots__:
            if _dict.has_key(attr):
                setattr(self, attr, _dict[attr])
            else:
                setattr(self, attr, None)

    def toJsonStr(self):
        tmpDict = self.toDict()

        if self.getChannel() is not None:
            tmpDict['Channel'] = self.getChannel().toDict()

        return json.dumps(tmpDict)

    def readJson(self, jsonStr):
        tmpDict = json.loads(jsonStr)

        self.readDict(tmpDict)
        tmpChannel = Channel()
        tmpChannel.readDict(tmpDict['Channel'])
        self.setChannel(tmpChannel)

    def updateStatus(self, status, spMsgId=0):
        cur_time = str(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        self.setLastUpdateDate(cur_time)
        self.setStatus(status)
        self.setSpMsgId(spMsgId)

    def updateStatus2Gataway(self, spMsgId=0):
        '''
        update msg status to msg status: send to gataway success
        '''
        self.updateStatus(Message.SENDED_TO_GATAWAY, spMsgId)

    def updateStatus2GatawayError(self):
        '''
        update msg status to msg status: send to gataway error
        '''
        self.updateStatus(Message.SENDED_TO_GATAWAY_ERROR)

    def isInEffective(self, effective_secs=900):
        tmptime = time.strptime(self.getCreationDate(), "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(tmptime))
        if time.time() - effective_secs < timeStamp:
            return False
        else:
            return True


class Channel(object):
    __metaclass__ = M
    __slots__ = ['Key', 'Psw', 'ChannelId',
                 'Sign', 'Weight', 'SpEntry', 'SourceNum']

    def __init__(self):
        self.setKey(None)
        self.setPsw(None)
        self.setChannelId(None)
        self.setSign(None)
        self.setWeight(None)
        self.setSpEntry(None)
        self.setSourceNum(None)

    # sync with db channel, channel group, app tables
    def setValuesFromDB(self, _dict):
        self.setKey(_dict['key'])
        self.setPsw(_dict['psw'])
        self.setChannelId(_dict['channel_id'])
        self.setSign(_dict['sign'])
        self.setWeight(_dict['weight'])
        self.setSpEntry(_dict['sp_entry'])
        # self.setSourceNum(_dict['source_num'])

    def toDict(self):
        tmpDict = dict()
        for attr in Channel.__slots__:
            tmpDict[attr] = getattr(self, attr)
        return tmpDict

    def toJsonStr(self):
        tmpDict = self.toDict()
        return json.dumps(tmpDict)

    def readDict(self, _dict):
        for attr in Channel.__slots__:
            if _dict.has_key(attr):
                setattr(self, attr, _dict[attr])
            else:
                setattr(self, attr, None)

    def readJson(self, jsonStr):
        tmpDict = json.loads(jsonStr)
        self.readDict(tmpDict)


if __name__ == '__main__':
    m = Message()

    # print(m.toJsonStr())
    cdict = dict()
    cdict['Key'] = 'vkey'
    cdict['Psw'] = 'vpws'
    cdict['ChannelId'] = 'vchanel'
    cdict['Sign'] = 'vsign'
    cdict['Weight'] = 'vweight'
    cdict['SpEntry'] = 'vspentry'
    cdict['SourceNum'] = 'vsourcenum'

    print cdict

    c = Channel()
    print c.toJsonStr()
    c.readDict(cdict)
    js = c.toJsonStr()
    print js
    c.readJson(js)
    print c.toJsonStr()
    print c.toDict()

    m = Message()
    print m.toJsonStr()
    m.setChannel(c)
    print m.toJsonStr()

    print m.toDict()

    mdict = {'Status': 'dddd', 'Language': 'ssss', 'SendId': 'sdfsdf',
             'Mobile': None, 'Method': None, 'LastUpdateDate':
             None, 'SqlTable': None, 'PhoneType': None, 'Msg': None, 'CreationDate': None,
             'Id': None, 'IsVerify': None, 'Channel': c}

    m.readDict(mdict)

    print m.toDict()
    print m.toJsonStr()

    js = '{"Status": "dddd", "Language": "ssss", "SendId": "sdfsdf", "Mobile": null, "Method": null, "LastUpdateDate": null, "SqlTable": null, "PhoneType": null, "Msg": null, "CreationDate": null, "Id": null, "Channel": {"SpEntry": "vspentry", "Psw": "vpws", "Weight": "vweight", "ChannelId": "vchanel", "Sign": "vsign", "Key": "vkey", "SourceNum": "vsourcenum"}, "IsVerify": null}'

    m.readJson(js)
    print m.toDict()

    print m.getChannel().toDict()

    m.updateStatus2Gataway()
    print m.toDict()

    m.updateStatus2Gataway(spMsgId=10000)
    print m.toDict()

    m = Message()
    m.setCreationDate('2015-01-01 00:00:00')
    print str(m.isInEffective())

    m.updateStatus2GatawayError()
    print m.toDict()
