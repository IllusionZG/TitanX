# -*- coding: utf-8 -*-
from akad import TalkService
from akad.ttypes import Message
from .auth import Auth
from .models import Models
from .talk import Talk
from .square import Square
from .call import Call
from .timeline import Timeline
from .liff import Liff
from .session import Session
from .server import Server
from akad.ttypes import DeviceInfo
import requests
import random, json, requests
import hashlib


def generateUID():
    androidId = ""
    seed = "1234567890asdfghjklzxcvbnmqwertyuiop"
    for lol in range(30):
        androidId += random.choice(seed)
    return "3f" + androidId

header = {
    'Accept': "application/json",
    "Accept-Language": "id-ID",
    "X-LHM": 'POST',
    "X-LPV": '1',
    "X-Line-Application": "BIZANDROID\t1.7.2\tANDROID_OS\t7.1.2",
    "User-Agent": "Line/8.11.0"
}
payload = {"deviceInfo":{"deviceName":"HM0373","model":"HM0373","udidHash":""},"deviceUid": generateUID()}

class LINE(Auth, Models, Talk, Square, Call, Timeline, Liff):

    def __init__(self):
        Auth.__init__(self)

    def deviceInfo(self, appType=32):
        return DeviceInfo(
            deviceName='HM0373',
            systemName='ANDROID',
            systemVersion='7.2.1',
            model='HM0373',
            carrierCode=0,
            carrierName='NOT_SPECIFIED',
            applicationType=appType)

    def register(self, seed=''):
        self.talk = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_API_QUERY_PATH_FIR).Talk()
        #res = requests.post('https://ga2s.line.naver.jp/plc/api/core/device/issueUdid', data=json.dumps(payload), #headers=header)
        #udidHash = res.json()['udidHash']
        #print(udidHash)
        udidHash = hashlib.md5( ('cool'+seed).encode() ).hexdigest()
        oldUdidHash = hashlib.md5( (udidHash).encode() ).hexdigest()
        return self.talk.registerDeviceWithoutPhoneNumber("JP", udidHash, self.deviceInfo())
		
    def login(self, idOrAuthToken=None, passwd=None, certificate=None, systemName=None, appName=None, showQr=False, keepLoggedIn=True):

        if not (idOrAuthToken or idOrAuthToken and passwd):
            self.loginWithQrCode(keepLoggedIn=keepLoggedIn, systemName=systemName, appName=appName, showQr=showQr)
        if idOrAuthToken and passwd:
            self.loginWithCredential(_id=idOrAuthToken, passwd=passwd, certificate=certificate, systemName=systemName, appName=appName, keepLoggedIn=keepLoggedIn)
        elif idOrAuthToken and not passwd:
            self.loginWithAuthToken(authToken=idOrAuthToken, appName=appName)

        self.__initAll()

    def __initAll(self):

        self.profile    = self.talk.getProfile()
        self.groups     = self.talk.getGroupIdsJoined()

        Liff.__init__(self)
        Models.__init__(self)
        Talk.__init__(self)
        #Square.__init__(self)
        #Call.__init__(self)
        #Timeline.__init__(self)
