#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkServerTransportSettingsSrv (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def GetSrvCertificate(self, szwCertType):
        data = {'szwCertType': szwCertType}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'ServerTransportSettingsSrv.GetSrvCertificate'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def GetSrvCertificateEx(self, szwCertType, pSettings):
        data = {'szwCertType': szwCertType, 'pSettings': pSettings}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'ServerTransportSettingsSrv.GetSrvCertificateEx'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

