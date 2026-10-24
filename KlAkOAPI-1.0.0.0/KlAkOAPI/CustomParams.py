#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkCustomParams (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def GetSettingsAndParams(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CustomParams.GetSettingsAndParams'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False, out_pars=['pSettings', 'pParams'])

    def SetSettingsAndParams(self, pSettings, pParams):
        data = {'pSettings': pSettings, 'pParams': pParams}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CustomParams.SetSettingsAndParams'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetValues(self, nDeviceId):
        data = {'nDeviceId': nDeviceId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CustomParams.GetValues'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def SetValues(self, nDeviceId, pValues):
        data = {'nDeviceId': nDeviceId, 'pValues': pValues}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CustomParams.SetValues'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

