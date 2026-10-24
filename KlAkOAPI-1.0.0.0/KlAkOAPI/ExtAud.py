#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkExtAud (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def GetRevision(self, nObjId, nObjType, nObjRevision):
        data = {'nObjId': nObjId, 'nObjType': nObjType, 'nObjRevision': nObjRevision}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'ExtAud.GetRevision'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False, out_pars=['pObjParams'])

    def UpdateRevisionDesc(self, nObjId, nObjType, nObjRevision, wstrNewDescription):
        data = {'nObjId': nObjId, 'nObjType': nObjType, 'nObjRevision': nObjRevision, 'wstrNewDescription': wstrNewDescription}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'ExtAud.UpdateRevisionDesc'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def FinalDelete(self, arrObjects):
        data = {'arrObjects': arrObjects}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'ExtAud.FinalDelete'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

