# -*- coding: utf-8 -*-
from akad.ttypes import *
from akad import LiffService

import json, ntpath

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other('You want to call the function, you must login to LINE')
    return checkLogin

class Liff(object):
    isLogin = False

    def __init__(self):
        self.isLogin = True

    @loggedIn
    def issueLiffView(self, request):
        return self.liff.issueLiffView(request)

    @loggedIn
    def revokeToken(self, request):
        return self.liff.revokeToken(request)
