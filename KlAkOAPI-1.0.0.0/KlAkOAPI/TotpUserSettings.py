#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkTotpUserSettings (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def ClearUserSecret(self, llTrusteeId):
        data = {'llTrusteeId': llTrusteeId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TotpUserSettings.ClearUserSecret'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def IfCanClearUser2FaSecret(self, llTrusteeId):
        data = {'llTrusteeId': llTrusteeId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TotpUserSettings.IfCanClearUser2FaSecret'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, out_pars=['bLoggedInUsing2FA'])

    def AddUserToTotpRequrementExceptions(self, llTrusteeId, bInExceptions):
        data = {'llTrusteeId': llTrusteeId, 'bInExceptions': bInExceptions}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TotpUserSettings.AddUserToTotpRequrementExceptions'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

