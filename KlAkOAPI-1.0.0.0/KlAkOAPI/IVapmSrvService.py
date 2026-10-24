#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkIVapmSrvService (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def SetProductAutoUpdateState(self, parProd):
        data = {'parProd': parProd}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IVapmSrvService.SetProductAutoUpdateState'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

