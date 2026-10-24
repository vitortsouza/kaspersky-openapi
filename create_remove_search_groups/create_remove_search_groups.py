# #!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
This module presents samples of usage KlAkOAPI package to deal with KSC group structure.
It has been updated to support argparse parameters for connection and to ignore SSL certificate verification.
"""

import sys
import time
import argparse
from getpass import getpass
import urllib3
import win32com.client

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.Params import KlAkParams, KlAkArray
from KlAkOAPI.Base import KlAkBase
from KlAkOAPI.Error import KlAkError
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.ChunkAccessor import KlAkChunkAccessor
from KlAkOAPI.AsyncActionStateChecker import KlAkAsyncActionStateChecker


def MillisecondsToSeconds(ms):
    return float(ms) / 1000.0


def PrintGroupsTree(arrGroups, nLevel):
    for group in arrGroups:
        nId = group['id']
        strName = group['name']
        strIndention = '    '
        for i in range(nLevel):
            strIndention += '  '
        strIndention += '+-'
        print(strIndention, 'Subgroup:', strName, ', id:', nId)
        if 'groups' in group:
            subgroups = group['groups']
            PrintGroupsTree(subgroups, nLevel + 1)


def Sample_EnumerateGroups(hostGroup):
    print('Enumerating subgroups in root group "Managed devices":')

    nRootGroupID = hostGroup.GroupIdGroups().RetVal()
    arrSubgroups = hostGroup.GetSubgroups(nRootGroupID, 0).RetVal()

    if arrSubgroups is None or len(arrSubgroups) == 0:
        print('Root group is empty')
    else:
        PrintGroupsTree(KlAkArray(arrSubgroups), 0)


def Sample_FindGroups(hostGroup, server, sFilter):
    print('Searching groups with filter "' + sFilter + '":')

    res = hostGroup.FindGroups(
        sFilter,
        vecFieldsToReturn=['id', 'name', 'grp_full_name', 'parentId', 'level'],
        vecFieldsToOrder=[],
        pParams={},
        lMaxLifeTime=100
    )

    print('Found ' + str(res.RetVal()) + ' groups:')
    strAccessor = res.OutPar('strAccessor')

    chunkAccessor = KlAkChunkAccessor(server)
    items_count = chunkAccessor.GetItemsCount(strAccessor).RetVal()

    start = 0
    step = 20000

    while start < items_count:
        res_chunk = chunkAccessor.GetItemsChunk(strAccessor, start, step)
        for group_param in KlAkArray(res_chunk.OutPar('pChunk')['KLCSP_ITERATOR_ARRAY']):
            print(group_param['grp_full_name'])
        start += step


def ProcessOU(hostGroup, nGroupID, command, strDN, nLevel):
    command.CommandText = (
        '<LDAP://' + strDN +
        '>;(&(objectCategory=organizationalUnit)(|(!(showInAdvancedViewOnly=*))(showInAdvancedViewOnly=0)));'
        'name, distinguishedName;oneLevel'
    )

    rs = command.Execute()[0]
    i = 0

    while not rs.EOF:
        strNewName = rs.Fields('name').Value
        strNewDN = rs.Fields('distinguishedName').Value

        print('  ' * nLevel, '+-', strNewName)

        nIdNewGroup = hostGroup.AddGroup({'name': str(strNewName), 'parentId': nGroupID})

        if nLevel < 2:
            ProcessOU(hostGroup, nIdNewGroup.RetVal(), command, strNewDN, nLevel + 1)

        if i > 2:
            return

        rs.MoveNext()
        i += 1


def Sample_Add_AD_Groups(hostGroup):
    print('Creating group structure based on AD organizational units')

    oRootDSE = win32com.client.GetObject('LDAP://RootDSE')
    strDefaultNamingContext = oRootDSE.Get('defaultNamingContext')

    print('- DefaultNamingContext:', strDefaultNamingContext)

    conn = win32com.client.Dispatch('ADODB.Connection')
    conn.Provider = 'ADSDSOObject'
    conn.Open('Active Directory Provider')

    command = win32com.client.Dispatch('ADODB.Command')
    command.ActiveConnection = conn

    print('- creating "process_ou" group')
    rootGroupId = hostGroup.GroupIdGroups().RetVal()
    nGroupId = hostGroup.AddGroup({'name': 'process_ou', 'parentId': rootGroupId}).RetVal()

    print('- iterating AD structure...')
    ProcessOU(hostGroup, nGroupId, command, strDefaultNamingContext, nLevel=1)

    conn.Close()

    print('Group structure successfully duplicated from AD')
    return nGroupId


def Sample_RemoveGroup(hostGroup, server, nGroupId):
    print('Removing group')

    groupInfo = hostGroup.GetGroupInfo(nGroupId).RetVal()
    print('Group to remove:', groupInfo['grp_full_name'])

    if nGroupId == hostGroup.GroupIdGroups().RetVal():
        print('Cannot delete root group')
        return

    res = hostGroup.RemoveGroup(nGroup=nGroupId, nFlags=1)
    strActionGuid = res.OutPar('strActionGuid')

    checker = KlAkAsyncActionStateChecker(server)

    while True:
        res = checker.CheckActionState(strActionGuid)

        if res.OutPar('bFinalized'):
            if res.OutPar('bSuccededFinalized'):
                print('Group deleted successfully')
            else:
                err = KlAkParams(res.OutPar('pStateData'))
                print('Error deleting group:', err['GNRL_EA_DESCRIPTION'])
            return
        else:
            time.sleep(MillisecondsToSeconds(res.OutPar('lNextCheckDelay')))


def Sample_AddGroup(hostGroup, sGroupName, nParentGroupId):
    print('Adding subgroup:', sGroupName)

    res = hostGroup.FindGroups('(name="' + sGroupName + '")', ['id'], [], {}, 100)
    if res.RetVal() > 0:
        print('Group', sGroupName, 'already exists')
        return

    nGroupId = hostGroup.AddGroup({'name': sGroupName, 'parentId': nParentGroupId}).RetVal()
    print('Group added successfully')
    return nGroupId


def main():
    print(main.__doc__)

    parser = argparse.ArgumentParser()

    # original flags
    parser.add_argument('-e', action='store_true', help='Enumerate groups')
    parser.add_argument('-f', metavar='FILTER', help='Search groups')
    parser.add_argument('-r', metavar='GROUP_ID', type=int, help='Remove group')
    parser.add_argument('-ou', action='store_true', help='Build group structure from AD OUs')
    parser.add_argument('-a', metavar='GROUP_NAME', help='Add subgroup')

    # new flags
    parser.add_argument('-server', required=True, help='KSC server URL, e.g. https://host:13299')
    parser.add_argument('-user', required=True, help='Username')
    parser.add_argument('-password', help='Password. If omitted, it will be requested')
    parser.add_argument('-ksc_user', action='store_true', help='Indicates KSC internal account')
    parser.add_argument('-domain', default="", help='AD domain (if not using -ksc_user)')
    parser.add_argument('-cert', help='Path to the KSC server CA certificate')
    parser.add_argument('-verify', action='store_true', help='Enable SSL verification')

    args = parser.parse_args()

    if args.user and args.password is None:
        args.password = getpass("Senha do KSC: ")

    # default action
    if not any([args.f, args.r, args.ou, args.a]):
        args.e = True

    # build username
    if args.ksc_user:
        username = args.user
    else:
        username = f"{args.domain}\\{args.user}" if args.domain else args.user

    verify = args.cert if args.cert else args.verify

    server = KlAkAdmServer.Create(
        args.server,
        username,
        args.password,
        verify=verify
    )

    hostGroup = KlAkHostGroup(server)

    if args.e:
        Sample_EnumerateGroups(hostGroup)

    if args.f:
        Sample_FindGroups(hostGroup, server, args.f)

    if args.ou:
        Sample_Add_AD_Groups(hostGroup)

    if args.r is not None:
        Sample_RemoveGroup(hostGroup, server, args.r)

    if args.a:
        Sample_AddGroup(hostGroup, args.a, hostGroup.GroupIdGroups().RetVal())


if __name__ == '__main__':
    main()