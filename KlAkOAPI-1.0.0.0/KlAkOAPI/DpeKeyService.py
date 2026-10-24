#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkDpeKeyService (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def GetDeviceKeys3(self, wstrDeviceId):
        data = {'wstrDeviceId': wstrDeviceId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'DpeKeyService.GetDeviceKeys3'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False, out_pars=['pKeyInfos'])

    def GetDevicesInfoForRemovedHosts(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'DpeKeyService.GetDevicesInfoForRemovedHosts'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False, out_pars=['pInfos'])

