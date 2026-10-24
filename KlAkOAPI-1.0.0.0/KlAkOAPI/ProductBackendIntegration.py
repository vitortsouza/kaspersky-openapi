#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkProductBackendIntegration (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def SetIntegrationToken(self, wstrProdName, wstrProdVersion, pRefreshToken, nTokenTtl):
        data = {'wstrProdName': wstrProdName, 'wstrProdVersion': wstrProdVersion, 'pRefreshToken': pRefreshToken, 'nTokenTtl': nTokenTtl}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'ProductBackendIntegration.SetIntegrationToken'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def DeleteIntegrationToken(self, wstrProdName, wstrProdVersion):
        data = {'wstrProdName': wstrProdName, 'wstrProdVersion': wstrProdVersion}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'ProductBackendIntegration.DeleteIntegrationToken'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def IfIntegrationAccessTokenValid(self, wstrProdName, wstrProdVersion):
        data = {'wstrProdName': wstrProdName, 'wstrProdVersion': wstrProdVersion}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'ProductBackendIntegration.IfIntegrationAccessTokenValid'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

