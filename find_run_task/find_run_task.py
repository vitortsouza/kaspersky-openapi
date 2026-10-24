#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""List, find, check status and run Kaspersky Security Center tasks."""

import argparse
import sys
import time
from pathlib import Path

import urllib3

from KlAkOAPI.Tasks import KlAkTasks
from KlAkOAPI.Params import KlAkParams, KlAkArray, paramParams
from KlAkOAPI.EventProcessing import KlAkEventProcessing

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ksc_common import add_connection_args, connect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ------------------------------------------------------------------------------
# SAFE ACCESS FOR KlAkParams
# ------------------------------------------------------------------------------
def get_param(obj, key, default=None):
    if isinstance(obj, KlAkParams) and key in obj:
        return obj[key]
    return default


# ------------------------------------------------------------------------------
# LIST ALL TASKS
# ------------------------------------------------------------------------------
def ListAllTasks(oTasks):
    print("\n=== TASK LIST ===\n")

    iterator = oTasks.ResetTasksIterator(
        nGroupId=0,
        bGroupIdSignificant=False,
        strProductName=None,
        strVersion=None,
        strComponentName=None,
        strInstanceId=None,
        strTaskName=None,
        bIncludeSupergroups=True
    ).OutPar("strTaskIteratorId")

    count = 0

    while True:
        data = oTasks.GetNextTask(iterator).OutPar("pTaskData")
        if not data:
            break

        info = get_param(data, "TASK_INFO_PARAMS")
        uid = get_param(data, "TASK_UNIQUE_ID")

        name = get_param(info, "DisplayName", "<unnamed>") if info else "<unnamed>"

        print(f"- {name} | UID: {uid}")
        count += 1

    oTasks.ReleaseTasksIterator(iterator)
    print(f"\n=== END OF LIST ({count} tasks) ===\n")


# ------------------------------------------------------------------------------
# FIND TASK BY NAME
# ------------------------------------------------------------------------------
def FindTaskByName(oTasks, name):
    name = name.lower()
    print("Searching for task by name:", name)

    iterator = oTasks.ResetTasksIterator(
        nGroupId=0, bGroupIdSignificant=False,
        strProductName=None, strVersion=None,
        strComponentName=None, strInstanceId=None,
        strTaskName=None, bIncludeSupergroups=True
    ).OutPar("strTaskIteratorId")

    while True:
        data = oTasks.GetNextTask(iterator).OutPar("pTaskData")
        if not data:
            break

        info = get_param(data, "TASK_INFO_PARAMS")
        uid = get_param(data, "TASK_UNIQUE_ID")

        task_name = get_param(info, "DisplayName") if info else None

        if task_name and task_name.lower() == name:
            print("Task found:", task_name, "| UID:", uid)
            oTasks.ReleaseTasksIterator(iterator)
            return uid

    oTasks.ReleaseTasksIterator(iterator)
    return None


# ------------------------------------------------------------------------------
# QUERY LAST TASK RESULT (WITHOUT RUNNING)
# ------------------------------------------------------------------------------
def GetLastTaskStatusWithoutRunning(server, oTasks, uid):
    fields = KlAkArray(['event_type', 'task_new_state', 'event_id', 'rise_time'])
    sort = KlAkArray([paramParams({'Name': 'rise_time', 'Asc': False})])
    flt = KlAkParams({'event_type': 'KLPRCI_TaskState'})

    history = oTasks.GetTaskHistory(uid, fields, sort, "", flt)
    iterator = history.OutPar("strIteratorId")

    processor = KlAkEventProcessing(server)
    count = processor.GetRecordCount(iterator).RetVal()

    if count == 0:
        processor.ReleaseIterator(iterator)
        return None

    events = processor.GetRecordRange(iterator, 0, 1).OutPar("pParamsEvents")
    processor.ReleaseIterator(iterator)

    if not events or "KLEVP_EVENT_RANGE_ARRAY" not in events:
        return None

    e = events["KLEVP_EVENT_RANGE_ARRAY"][0]

    return {
        "state": e["task_new_state"],
        "event_id": e["event_id"],
        "time": e["rise_time"],
        "raw": e
    }


# ------------------------------------------------------------------------------
# RUN TASK & WAIT FOR RESULT
# ------------------------------------------------------------------------------
def RunTaskAndReturnResult(server, oTasks, uid):
    info = oTasks.GetTask(uid).RetVal()

    name = info["DisplayName"]
    created = info["PRTS_TASK_CREATION_DATE"]

    print("\nRunning task:", name)
    print("Created at:", created)

    old_state = GetLastTaskStatusWithoutRunning(server, oTasks, uid)

    print("Executing...")
    oTasks.RunTask(uid)
    time.sleep(5)

    while True:
        new_state = GetLastTaskStatusWithoutRunning(server, oTasks, uid)

        if new_state and (old_state is None or new_state["event_id"] != old_state["event_id"]):
            print("Task finished with state:", new_state["state"])
            return new_state["state"]

        time.sleep(5)


# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Run or list KSC tasks")
    add_connection_args(parser)

    parser.add_argument("-list", action="store_true")
    parser.add_argument("-task", help="Task name to execute or check")
    parser.add_argument("-status", action="store_true", help="Show last task status")

    args = parser.parse_args()
    server = connect(args)
    print("Connected to", args.server)

    oTasks = KlAkTasks(server)

    # LISTAR
    if args.list:
        ListAllTasks(oTasks)
        return

    # TAREFAS (necessário nome da task)
    if not args.task:
        print("Error: you must specify -task NAME when using -status or running a task.")
        return

    # LOCALIZA A TASK
    task_uid = FindTaskByName(oTasks, args.task)
    if not task_uid:
        print("Task not found:", args.task)
        return

    # STATUS SEM EXECUTAR
    if args.status:
        status = GetLastTaskStatusWithoutRunning(server, oTasks, task_uid)
        if not status:
            print("No status found for this task.")
            return

        print("\n=== LAST TASK STATUS ===")
        print("State :", status["state"])
        print("Event :", status["event_id"])
        print("Time  :", status["time"])
        print("========================")
        return

    # EXECUTAR TASK
    result = RunTaskAndReturnResult(server, oTasks, task_uid)

    print("\n=== RESULT ===")
    print("SUCCESS" if result == 4 else "FAILED")
    print("==============")



if __name__ == "__main__":
    main()
