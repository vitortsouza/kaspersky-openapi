#! /usr/bin/python -tt

from .Base import KlAkBase
from .Params import KlAkParamsEncoder
import json

class KlAkMdmCertCtrlApi (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def SetCertificate(self, pAuthType, pNotification, pCertificate, pRecipients):
        data = {'pAuthType': pAuthType, 'pNotification': pNotification, 'pCertificate': pCertificate, 'pRecipients': pRecipients}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.SetCertificate'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def SetCertificateAsync(self, pAuthType, pNotification, pCertificate, pRecipient, wstrRequestId):
        data = {'pAuthType': pAuthType, 'pNotification': pNotification, 'pCertificate': pCertificate, 'pRecipient': pRecipient, 'wstrRequestId': wstrRequestId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.SetCertificateAsync'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def CancelSetCertificate(self, wstrRequestId):
        data = {'wstrRequestId': wstrRequestId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.CancelSetCertificate'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def SetCertificateAsync2(self, pAuthType, pNotification, pCertificate, pRecipient):
        data = {'pAuthType': pAuthType, 'pNotification': pNotification, 'pCertificate': pCertificate, 'pRecipient': pRecipient}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.SetCertificateAsync2'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False, out_pars=['wstrRequestId'])

    def CancelSetCertificate2(self, wstrRequestId):
        data = {'wstrRequestId': wstrRequestId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.CancelSetCertificate2'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GeneratePackage(self, pPackageInfo, pCertificate, pRecipients, pNotification):
        data = {'pPackageInfo': pPackageInfo, 'pCertificate': pCertificate, 'pRecipients': pRecipients, 'pNotification': pNotification}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GeneratePackage'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GeneratePackageAsync(self, pPackageInfo, pCertificate, pRecipients, pNotification, wstrRequestId):
        data = {'pPackageInfo': pPackageInfo, 'pCertificate': pCertificate, 'pRecipients': pRecipients, 'pNotification': pNotification, 'wstrRequestId': wstrRequestId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GeneratePackageAsync'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def CancelGeneratePackage(self, wstrRequestId):
        data = {'wstrRequestId': wstrRequestId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.CancelGeneratePackage'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GeneratePackageAsync2(self, pPackageInfo, pCertificate, pRecipients, pNotification):
        data = {'pPackageInfo': pPackageInfo, 'pCertificate': pCertificate, 'pRecipients': pRecipients, 'pNotification': pNotification}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GeneratePackageAsync2'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False, out_pars=['wstrRequestId'])

    def CancelGeneratePackage2(self, wstrRequestId):
        data = {'wstrRequestId': wstrRequestId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.CancelGeneratePackage2'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def RenewCertificate(self, nCertId, pCertificate):
        data = {'nCertId': nCertId, 'pCertificate': pCertificate}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.RenewCertificate'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def SetCertificateTag(self, nCertId, wstrCertTag):
        data = {'nCertId': nCertId, 'wstrCertTag': wstrCertTag}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.SetCertificateTag'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def SetIOSMDMProfile(self, pProfileInfo, pCertificate, pRecipients, pNotification):
        data = {'pProfileInfo': pProfileInfo, 'pCertificate': pCertificate, 'pRecipients': pRecipients, 'pNotification': pNotification}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.SetIOSMDMProfile'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetRestoreData(self, wstrDeviceHostName):
        data = {'wstrDeviceHostName': wstrDeviceHostName}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GetRestoreData'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False, out_pars=['pRestoreData'])

    def DeleteCertificates(self, pIds):
        data = {'pIds': pIds}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.DeleteCertificates'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetCertificatePublic(self, nCertId):
        data = {'nCertId': nCertId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GetCertificatePublic'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def CheckPkiEnabled(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.CheckPkiEnabled'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def CheckPkiAccount(self, wsAccountName, pAccountPwd, wsHostName):
        data = {'wsAccountName': wsAccountName, 'pAccountPwd': pAccountPwd, 'wsHostName': wsHostName}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.CheckPkiAccount'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def GetPkiTemplates(self, bForceReload):
        data = {'bForceReload': bForceReload}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GetPkiTemplates'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def GetPkiTemplatesByEKU(self, wsEKU, bForceReload):
        data = {'wsEKU': wsEKU, 'bForceReload': bForceReload}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GetPkiTemplatesByEKU'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def IsPkiCertificateRevokedById(self, nCertId):
        data = {'nCertId': nCertId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.IsPkiCertificateRevokedById'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def IsPkiCertificateRevoked(self, pCertPublic):
        data = {'pCertPublic': pCertPublic}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.IsPkiCertificateRevoked'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def UpdateIssuanceSettings(self, pCertTypes):
        data = {'pCertTypes': pCertTypes}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.UpdateIssuanceSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetIssuanceSettings(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GetIssuanceSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def GetIssuanceSettingsByType(self, nCertType):
        data = {'nCertType': nCertType}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GetIssuanceSettingsByType'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def GetPackagesByPackageProduct(self, wsPkgProductName, wsPkgProductVersion):
        data = {'wsPkgProductName': wsPkgProductName, 'wsPkgProductVersion': wsPkgProductVersion}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GetPackagesByPackageProduct'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def CheckMailNotificationSettings(self, bCheckMainServerDefaults):
        data = {'bCheckMainServerDefaults': bCheckMainServerDefaults}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.CheckMailNotificationSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def GetPkiAgentSettings(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.GetPkiAgentSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text)

    def SetPkiAgentSettings(self, pSettings):
        data = {'pSettings': pSettings}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'MdmCertCtrlApi.SetPkiAgentSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder), verify = self.server.session.verify)
        return self.ParseResponse(response.status_code, response.text, retval = False)

