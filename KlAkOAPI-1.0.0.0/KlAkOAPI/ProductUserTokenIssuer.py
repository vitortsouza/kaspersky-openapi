#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkProductUserTokenIssuer (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def IssueUserToken(self, wstrProductName, wstrProductVersion):
        data = {'wstrProductName': wstrProductName, 'wstrProductVersion': wstrProductVersion}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'ProductUserTokenIssuer.IssueUserToken'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def RevokeUserToken(self, wstrProductName, wstrProductVersion):
        data = {'wstrProductName': wstrProductName, 'wstrProductVersion': wstrProductVersion}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'ProductUserTokenIssuer.RevokeUserToken'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

