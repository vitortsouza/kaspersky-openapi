# #!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import argparse
import urllib3
import socket
import re
from pathlib import Path
from getpass import getpass
import logging
from sys import platform
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.Base import MillisecondsToSeconds
from KlAkOAPI.Params import (
    KlAkParams,
    KlAkArray,
    paramArray,
    paramParams,
    paramDateTime,
    dateToStr,
    dateTimeToStr,
    paramString,
)
from KlAkOAPI.SrvView import KlAkSrvView
from KlAkOAPI.FileCategorizer2 import KlAkFileCategorizer2

# import keyring

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PORT = 13299

EX_TYPE = 3
STR_OP = 0


def ConnectServer(server_url, username=None, password=None, ksc_user=False, cert=False):
    try:
        """Connects to main KSC server"""
        server = KlAkAdmServer.Create(
            server_url, username, password, internal_user=ksc_user, verify=cert
        )
        logging.info("KSC server connection successfully!")
        return server
    except Exception as e:
        logging.error(e)
        return None


def CheckCategory(server, name):
    try:
        oSrvView = KlAkSrvView(server)
        strSrvViewName = "customcategories"
        oFields2Return = KlAkArray(["id", "name"])
        oField2Order = KlAkArray([])
        wstrIteratorId = oSrvView.ResetIterator(
            strSrvViewName,
            '(name = "' + name + '")',
            oFields2Return,
            oField2Order,
            {},
            lifetimeSec=60 * 60 * 3,
        ).OutPar("wstrIteratorId")
        iRecordCount = oSrvView.GetRecordCount(wstrIteratorId).RetVal()
        iStep = 200
        iStart = 0
        if iRecordCount > 0:
            while iStart < iRecordCount:
                pRecords = oSrvView.GetRecordRange(
                    wstrIteratorId, iStart, iStart + iStep
                ).OutPar("pRecords")
                i = 0
                for oObj in pRecords["KLCSP_ITERATOR_ARRAY"]:
                    logging.debug(oObj)
                    nCategoryId = oObj["id"]
                    return {"bResult": True, "nCategoryId": nCategoryId}
                iStart += iStep + 1
        else:
            return {"bResult": False}

    except Exception as e:
        logging.error(e)
        return None
    finally:
        oSrvView.ReleaseIterator(wstrIteratorId)


def mergeInclusions(oCatProps, inclusions_list):
    try:
        hash_sha256 = {}
        is_changed = False
        for category_item in oCatProps["inclusions"]:
            if "str2" in category_item["value"]:
                hash_sha256[category_item["value"]["str2"]] = True
        for hash_item in inclusions_list:
            if hash_item["value"]["str2"] in hash_sha256:
                continue
            else:
                oCatProps["inclusions"].append(hash_item)
                is_changed = True
                logging.info(f"Append {hash_item['value']['str2']}")
                print(f"Append {hash_item['value']['str2']}")

        return {"is_changed": is_changed, "oCatProps": oCatProps}
    except Exception as e:
        logging.error(e)
        return None


def AddArgs(parser):
    group_address = parser.add_argument_group()
    group_address.add_argument(
        "-server",
        action="store",
        help='(optional) address where KSC server is located, for example "https://ksc.example.com:13299". If no -address option is used, suppose KSC server is installed on current machine',
    )
    
    # group_address.add_argument(
    #     "-app_name", action="store", help="Item name of credential manager"
    # )

    group_address.add_argument(
        "-user", action="store", help="account for auth on KSC server"
    )
    group_address.add_argument(
        "-password",
        action="store",
        help="password to account for basic auth on KSC server",
    )
    group_address.add_argument(
        "-ksc_user", action="store_true", help="set for internal ksc account"
    )
    group_address.add_argument(
        "-cert", action="store", help="Path to certificate file of main server"
    )
    group_address.add_argument("-file", action="store", help="input file")
    group_address.add_argument("-category", action="store", help="category name")
    group_address.add_argument(
        "-full_replace",
        action="store_true",
        help="set the argument, if conditions from the category must be removed. (By default, conditions are added to the category)",
    )
    group_address.add_argument("-d", action="store_true", help="debug mode log")
    return


def main():
    """ """
    parser = argparse.ArgumentParser(description="")

    AddArgs(parser)
    args = parser.parse_args()
    if args.d == None:
        logging_level = logging.INFO
    if args.d == True:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logging.basicConfig(
        level=logging_level,
        filename=f"{Path(__file__).stem}.log",
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
    )

    server_address = args.server

    match server_address:
        case None:
            server_address = f"{socket.getfqdn()}:{PORT}"
            server_url = f"https://{server_address}"
        case _:
            server_url = server_address

    match args.cert:
        case None:
            cert = False
        case _:
            cert = args.cert

    match args.ksc_user:
        case None:
            is_ksc_user = False
        case _:
            is_ksc_user = args.ksc_user

    match args.full_replace:
        case None:
            is_full_replace = False
        case _:
            is_full_replace = args.full_replace

    user = args.user
    password = args.password

    category_name = args.category

    file = args.file

    user = args.user
    password = args.password

    # app_name = args.app_name

    # if app_name != None:
    #     user_password = keyring.get_password(app_name, user)
    #     if user_password != None:
    #         password = user_password

    if user != None and password == None:
        password = getpass(prompt="Please input Password : ")

    server_main = ConnectServer(server_url, user, password, is_ksc_user, cert)

    oFileCategorizer2 = KlAkFileCategorizer2(server_main)

    hash_regex = re.compile(r"^[a-f0-9]{64}$", re.IGNORECASE)
    inclusions_list = []
    with open(file, "r") as file:
        while line := file.readline():
            sha256 = line.rstrip().lower()
            if re.fullmatch(hash_regex, sha256):
                inclusions_list.append(
                    {
                        "type": "params",
                        "value": {"ex_type": EX_TYPE, "str2": sha256, "str_op": STR_OP},
                    }
                )
            else:
                logging.warning(f"Hash {sha256} invalid. Skiped")

    oCategory = CheckCategory(server_main, category_name)

    if oCategory["bResult"]:
        logging.info(f"Found category: {category_name} id: {oCategory['nCategoryId']}")
        print((f"Found category: {category_name} id: {oCategory['nCategoryId']}"))

        oCategoryData = oFileCategorizer2.GetCategory(oCategory["nCategoryId"])
        oCatProps = oCategoryData.respose_text["pCategory"]
        strAction = ""
        if is_full_replace:
            oCatProps["inclusions"] = inclusions_list
            strAction = "replaced"
        else:
            mergeResult = mergeInclusions(oCatProps, inclusions_list)
            if "is_changed" in mergeResult:
                if mergeResult["is_changed"]:
                    oCatProps = mergeResult["oCatProps"]
                    strAction = "updated"
                else:
                    logging.warning(f'Nothing to update category "{category_name}"')
                    print(f'Nothing to update category "{category_name}"')

        if strAction != "":
            oFileCategorizer2.UpdateCategory(oCategory["nCategoryId"], oCatProps)
            logging.info(f'Category "{category_name}" {strAction}')
            print(f'Category "{category_name}" {strAction}')
    else:
        oCatProps = {
            "CategoryType": 0,
            "name": category_name,
            "inclusions": inclusions_list,
        }

        oFileCategorizer2.CreateCategory(oCatProps)
        logging.info(f"Create category: {category_name}")
        print("Create category: " + category_name)

    logging.info("Ok")


if __name__ == "__main__":
    main()
