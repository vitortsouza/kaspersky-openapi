#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""This module presents samples of usage KlAkOAPI package to add internal user"""

import socket
import uuid
import datetime
import argparse
from getpass import getpass
from sys import platform
import urllib3

# Disable SSL warnings (certificado inseguro)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from KlAkOAPI.Params import KlAkArray, paramBinary, strToBin, dateTimeToStr
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.SecurityPolicy import KlAkSecurityPolicy
from KlAkOAPI.DataProtectionApi import KlAkDataProtectionApi


def GetServer(server_url, username, password, is_internal_user, verify=False):
    """Connects to KSC server"""

    # Autenticação NTLM no Windows se não for conta interna
    if platform == "win32" and not is_internal_user:
        username = None
        password = None

    return KlAkAdmServer.Create(server_url, username, password, verify=verify)


def parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description="Add internal user to Kaspersky Security Center via KlAkOAPI")

    # Parâmetros de conexão
    parser.add_argument("-server", "--server", required=True,
                        help="URL do servidor, ex: https://endereco:13299")
    parser.add_argument("-user", "--user",
                        help="Usuário para autenticação no KSC")
    parser.add_argument("-password", "--password",
                        help="Senha para autenticação no KSC")
    parser.add_argument("-ksc_user", "--ksc_user",
                        action="store_true",
                        help="Indica que a autenticação é por conta interna (não NTLM)")
    parser.add_argument("-cert", "--cert",
                        help="Caminho do certificado CA do servidor")
    parser.add_argument("-verify", "--verify",
                        action="store_true",
                        help="Habilita a verificação SSL")

    # Parâmetros da nova conta interna
    parser.add_argument("-new_user", "--new_user", required=True,
                        help="Nome do novo usuário interno a ser criado")
    parser.add_argument("-new_password", "--new_password",
                        help="Senha do novo usuário interno. Se omitida, será solicitada")

    return parser.parse_args()


def main():
    """Create internal user on KSC"""
    print(main.__doc__)

    args = parse_args()

    if args.user and args.password is None:
        args.password = getpass("Senha do KSC: ")
    if args.new_password is None:
        args.new_password = getpass("Senha do novo usuário: ")

    verify = args.cert if args.cert else args.verify

    server = GetServer(
        server_url=args.server,
        username=args.user,
        password=args.password,
        is_internal_user=args.ksc_user,
        verify=verify
    )

    # Criptografar a senha do usuário novo
    oDataProtectionApi = KlAkDataProtectionApi(server)
    bPasswordProtected = oDataProtectionApi.ProtectUtf16StringGlobally(args.new_password).RetVal()

    # Criar usuário
    oUsers = KlAkSecurityPolicy(server)

    nUserID = oUsers.AddUser({
        "KLSPL_USER_NAME": args.new_user,
        "KLSPL_USER_FULL_NAME": args.new_user,
        "KLSPL_USER_PWD_ENCRYPTED": paramBinary(bPasswordProtected)
    }).RetVal()

    print(f"Usuário interno criado: {args.new_user}, ID = {nUserID}")


if __name__ == '__main__':
    main()