#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkSrvIpmNewsAndStatistics (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def SendStatistics(self, pwchContentId, parOptionalInfo):
        data = {'pwchContentId': pwchContentId, 'parOptionalInfo': parOptionalInfo}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'SrvIpmNewsAndStatistics.SendStatistics'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetTrackingData(self, pwchContentId):
        data = {'pwchContentId': pwchContentId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'SrvIpmNewsAndStatistics.GetTrackingData'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

