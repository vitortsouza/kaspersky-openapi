#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkIWebSrvRemoteSettings (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def GetCertificateInfo(self, wstrHostId):
        data = {'wstrHostId': wstrHostId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.GetCertificateInfo'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def SetCustomCertificate(self, wstrHostId, pCertData):
        data = {'wstrHostId': wstrHostId, 'pCertData': pCertData}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.SetCustomCertificate'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetCustomPkgHttpFqdn(self, wstrHostId):
        data = {'wstrHostId': wstrHostId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.GetCustomPkgHttpFqdn'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def SetCustomPkgHttpFqdn(self, wstrHostId, wsFqdn):
        data = {'wstrHostId': wstrHostId, 'wsFqdn': wsFqdn}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.SetCustomPkgHttpFqdn'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetRemoteWebServerHosts(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.GetRemoteWebServerHosts'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def IsHostWebServer(self, wstrHostId):
        data = {'wstrHostId': wstrHostId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.IsHostWebServer'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def SetRemoteWebServerHosts(self, pHostsData):
        data = {'pHostsData': pHostsData}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.SetRemoteWebServerHosts'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def SetWebSrvRemoteSettings(self, wstrHostId, pSettings):
        data = {'wstrHostId': wstrHostId, 'pSettings': pSettings}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.SetWebSrvRemoteSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetWebSrvRemoteSettings(self, wstrHostId):
        data = {'wstrHostId': wstrHostId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.GetWebSrvRemoteSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

