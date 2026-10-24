#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkSpamEvents (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def GetSpamList(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'SpamEvents.GetSpamList'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def RemoveFromSpamList(self, pArraySpamEventIds):
        data = {'pArraySpamEventIds': pArraySpamEventIds}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'SpamEvents.RemoveFromSpamList'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def AddToExclusion(self, pArraySpamEventIds):
        data = {'pArraySpamEventIds': pArraySpamEventIds}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'SpamEvents.AddToExclusion'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def RemoveFromExclusion(self, pArraySpamEventIds):
        data = {'pArraySpamEventIds': pArraySpamEventIds}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'SpamEvents.RemoveFromExclusion'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

