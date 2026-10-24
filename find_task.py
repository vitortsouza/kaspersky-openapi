# #!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""This module presents samples of usage KlAkOAPI package to find and execute task by name"""

import argparse
import time

import urllib3

from KlAkOAPI.Params import KlAkParams, KlAkArray, paramParams
from KlAkOAPI.Tasks import KlAkTasks
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.EventProcessing import KlAkEventProcessing
from ksc_common import add_connection_args, connect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
def ListAllTasks(server):
    oTasks = KlAkTasks(server)
    strIt = oTasks.ResetTasksIterator(
        nGroupId=0,
        bGroupIdSignificant=False,
        strProductName=None,
        strVersion=None,
        strComponentName=None,
        strInstanceId=None,
        strTaskName=None,
        bIncludeSupergroups=True
    ).OutPar("strTaskIteratorId")

    print("\n=== LISTA DE TAREFAS ENCONTRADAS NO KSC ===\n")

    while True:
        task = oTasks.GetNextTask(strIt).OutPar("pTaskData")
        if not task:
            break

        try:
            name = task["TASK_INFO_PARAMS"]["DisplayName"]
            task_id = task["TASK_UNIQUE_ID"]
            print(f"- {name}   (ID: {task_id})")
        except:
            print("Task sem nome legível:", task)

    oTasks.ReleaseTasksIterator(strIt)
'''
    
def FindTask(oTasks, strDisplayName):
    print('Searching for task', strDisplayName)
    strTaskIteratorId = oTasks.ResetTasksIterator(nGroupId=0, bGroupIdSignificant=False, strProductName=None, strVersion=None, strComponentName=None, strInstanceId=None, strTaskName=None, bIncludeSupergroups=True).OutPar("strTaskIteratorId")       
    nTaskId = None
    while True:
        pTaskData = oTasks.GetNextTask(strTaskIteratorId).OutPar('pTaskData')
        if pTaskData == None or len(pTaskData) == 0:
            break
        strDN = pTaskData['TASK_INFO_PARAMS']['DisplayName']
        if strDN == strDisplayName:
            print('Task ' + strDN + ' found')
            nTaskId = pTaskData['TASK_UNIQUE_ID']
            break
                        
    oTasks.ReleaseTasksIterator(strTaskIteratorId)
    return nTaskId


def GetLastTaskResult(server, oTasks, strID):
    ''' Prints task history and returns last state '''
    #fill object with required fields
    oFields2Return = KlAkArray(['event_type', 'task_new_state', 'event_id', 'rise_time'])

    #sort descending by publication time
    oSortFields = KlAkArray([paramParams({'Name': 'rise_time', 'Asc' : False})])

    #we need only task state events
    oFilter = KlAkParams({'event_type': 'KLPRCI_TaskState'})

    oHistory = oTasks.GetTaskHistory(strID, oFields2Return, oSortFields, '', oFilter)

    oResult = None
    strIteratorId = oHistory.OutPar('strIteratorId')
    oEventProcessing = KlAkEventProcessing(server)
    if oEventProcessing.GetRecordCount(strIteratorId).RetVal() > 0:
        pParamsEvents = oEventProcessing.GetRecordRange  ( strIteratorId,  0,  oEventProcessing.GetRecordCount(strIteratorId).RetVal() ).OutPar('pParamsEvents')
        if pParamsEvents != None and 'KLEVP_EVENT_RANGE_ARRAY' in pParamsEvents:
            for item in pParamsEvents['KLEVP_EVENT_RANGE_ARRAY']:
                print('--- event --')
                print( 'event_id: ', item['event_id'],  '\tevent_type: ', item['event_type'], '\ttask_new_state: ', item['task_new_state'], '\trise_time: ', item['rise_time'])

                nState = item['task_new_state']
                if 3 == nState or 4 == nState : # if failed or completed successfully
                    oResult = item
                    break
                
        oEventProcessing.ReleaseIterator(strIteratorId)

    return oResult

def RunTaskAndReturnResult(server, oTasks, strID):
    ''' Runs task and checks for result '''
    oInfo = oTasks.GetTask(strID).RetVal()
    print(   'Processing task ' + oInfo['DisplayName'] + ' created at ' + oInfo['PRTS_TASK_CREATION_DATE'].isoformat() )

    # print task statistics into the log
    oStatistics = oTasks.GetTaskStatistics(strID).RetVal()

    print( 'Task statistics' )
    print( 'Not distributed: ', oStatistics['1'])
    print( 'Running: ', oStatistics['2'])
    print( 'OK: ', oStatistics['4'])
    print( 'Warning: ', oStatistics['8'])
    print( 'Failed: ', oStatistics['16'])
    print( 'Scheduled: ', oStatistics['32'])
    print( 'Paused: ', oStatistics['64'])

    #initial task state (before task start)
    oState0 = GetLastTaskResult(server, oTasks, strID)

    oTasks.RunTask( strID )

    # wait for a 5 seconds
    time.sleep(5)

    nResult = None
    while True:
        oState1 = GetLastTaskResult(server, oTasks, strID)
        if  ( None == oState0 and None != oState1) or ( None != oState1 and  None != oState0 and  oState1['event_id'] != oState0['event_id']):
            print('Task result is ', oState1['task_new_state'])
            nResult = oState1['task_new_state']
            break
        time.sleep(5)

    # return final task state (before task start)
    return nResult
    
    
def main():
    """ This sample shows how you can find and execute task """
    print (main.__doc__)

    parser = argparse.ArgumentParser(description="Encontra e executa uma tarefa do KSC pelo nome.")
    add_connection_args(parser)
    parser.add_argument(
        "-task",
        default="Optimized Full Scan - KES",
        help="Nome da tarefa a ser localizada e executada",
    )
    args = parser.parse_args()
    server = connect(args)

    '''
    ListAllTasks(server)
    return
    '''

    oHostGroup = KlAkHostGroup(server)
    nRootGroupId = oHostGroup.GroupIdGroups().RetVal()
    
    oTasks = KlAkTasks(server)
    strInterestingTaskName = args.task
    strFoundTask = FindTask(oTasks, strInterestingTaskName)
    if strFoundTask == None or  strFoundTask == '': 
        print('Task', strInterestingTaskName, 'not found')
    else:
        nResult = RunTaskAndReturnResult(server, oTasks, strFoundTask)
        if 4 == nResult:
            print('Task result is Success')
        else:
            print('Task result is Failure')


    
if __name__ == '__main__':
    main()
