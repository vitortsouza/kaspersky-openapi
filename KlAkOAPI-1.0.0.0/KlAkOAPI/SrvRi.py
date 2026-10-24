#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkSrvRi (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def SetRiTaskResults(self, wstrHostID, pData):
        data = {'wstrHostID': wstrHostID, 'pData': pData}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'SrvRi.SetRiTaskResults'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def ShouldForceReboot(self, wstrHostID, wstrTaskID):
        data = {'wstrHostID': wstrHostID, 'wstrTaskID': wstrTaskID}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'SrvRi.ShouldForceReboot'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def ShouldForceReboot2(self, wstrHostID, wstrTaskID):
        data = {'wstrHostID': wstrHostID, 'wstrTaskID': wstrTaskID}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'SrvRi.ShouldForceReboot2'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def SetRebootConfirmedHosts(self, pHostsArray):
        data = {'pHostsArray': pHostsArray}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'SrvRi.SetRebootConfirmedHosts'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

