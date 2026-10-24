#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkTestServerTransportSettings (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def TestGetSrvCertificate(self, nMethod, szwCertType):
        data = {'nMethod': nMethod, 'szwCertType': szwCertType}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestServerTransportSettings.TestGetSrvCertificate'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def TestSetCurrentTime(self, szwCertType, tTime):
        data = {'szwCertType': szwCertType, 'tTime': tTime}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestServerTransportSettings.TestSetCurrentTime'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

