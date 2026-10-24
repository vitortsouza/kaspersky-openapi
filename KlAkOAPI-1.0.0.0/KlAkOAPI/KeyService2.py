#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkKeyService2 (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def ExportDpeKeys(self, pEncryptedData):
        data = {'pEncryptedData': pEncryptedData}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'KeyService2.ExportDpeKeys'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False, out_pars=['pEncryptedKeysData'])

    def ImportDpeKeys(self, pEncryptedData, pEncryptedKeysData):
        data = {'pEncryptedData': pEncryptedData, 'pEncryptedKeysData': pEncryptedKeysData}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'KeyService2.ImportDpeKeys'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

