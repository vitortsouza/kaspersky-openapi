#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkTotpGlobalSettings (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def Set2FaRequiredForAll(self, bRequiredForAll):
        data = {'bRequiredForAll': bRequiredForAll}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TotpGlobalSettings.Set2FaRequiredForAll'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def Get2FaRequiredForAll(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TotpGlobalSettings.Get2FaRequiredForAll'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def SetTotpGlobalSettings(self, pSettings):
        data = {'pSettings': pSettings}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TotpGlobalSettings.SetTotpGlobalSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetTotpGlobalSettings(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TotpGlobalSettings.GetTotpGlobalSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False, out_pars=['pSettings'])

    def IfCanConfigure2FaSettings(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TotpGlobalSettings.IfCanConfigure2FaSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, out_pars=['bLoggedInUsing2FA'])

