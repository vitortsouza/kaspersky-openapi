#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkHostTagsApi (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def GetHostTags(self, szwHostId, pParams):
        data = {'szwHostId': szwHostId, 'pParams': pParams}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'HostTagsApi.GetHostTags'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def GetHostsTags(self, pArrHostIds, pParams):
        data = {'pArrHostIds': pArrHostIds, 'pParams': pParams}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'HostTagsApi.GetHostsTags'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

