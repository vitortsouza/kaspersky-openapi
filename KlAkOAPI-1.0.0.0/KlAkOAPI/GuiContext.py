#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkGuiContext (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def SetLanguage(self, pwchIetfLanguageTag):
        data = {'pwchIetfLanguageTag': pwchIetfLanguageTag}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'GuiContext.SetLanguage'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

