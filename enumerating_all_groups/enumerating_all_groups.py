# #!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""This module presents samples of usage KlAkOAPI package to enumerate groups with command-line arguments"""

import argparse
import socket
import logging
from sys import platform
from pathlib import Path
from getpass import getpass

# Importações específicas do KSC OAPI
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.Params import KlAkArray # Importado do script de enumeração [7]

# Importação para lidar com avisos de segurança
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # [1]

PORT = 13299 # [1]

def ConnectServer(server_url, username=None, password=None, ksc_user=False, cert=False):
    """Connects to main KSC server""" # [1]
    try:
        server = KlAkAdmServer.Create(
            server_url, username, password, internal_user=ksc_user, verify=cert
        )
        logging.info("KSC server connection successfully!") # [1]
        return server
    except Exception as e:
        logging.error(e) # [1]
        return None

def AddArgs(parser):
    """Define os argumentos esperados na linha de comando."""
    group_address = parser.add_argument_group() # [8]

    group_address.add_argument(
        "-server",
        action="store",
        help='(optional) address where KSC server is located, for example "https://ksc.example.com:13299". If no -server option is used, suppose KSC server is installed on current machine', # [4]
    )

    group_address.add_argument(
        "-user", action="store", help="account for auth on KSC server" # [4]
    )

    group_address.add_argument(
        "-password",
        action="store",
        help="password to account for basic auth on KSC server", # [5]
    )

    group_address.add_argument(
        "-ksc_user", action="store_true", help="set for internal ksc account" # [5]
    )
    
    # Mantemos o argumento de debug
    group_address.add_argument("-d", action="store_true", help="debug mode log") # [6]

    return

def EnumerateGroups(oGroups, nLevel):
    """Função recursiva para enumerar e imprimir os grupos.""" # [2]
    for oGroup in oGroups:
        nId = oGroup['id'] # [2]
        strName = oGroup['name'] # [2]

        # form indention for logging
        strIndention = ' ' + ' ' * nLevel + '+-' # [2]

        # log found group
        print(strIndention, 'Subgroup:', strName, ', id:', nId) # [2]

        if 'groups' in oGroup: # [2]
            groups = oGroup['groups'] # [2]
            EnumerateGroups(groups, nLevel + 1) # [2]

def main():
    """ This sample shows how you can enumerate groups using command-line arguments for connection """
    print (main.__doc__) # [3]

    # 1. Configurar Argumentos e Parsing
    parser = argparse.ArgumentParser(description="") # [6]
    AddArgs(parser) # [6]
    args = parser.parse_args() # [6]

    # 2. Configurar Logging (Baseado em add_category.py)
    if args.d == True:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    # Configuração de logging padrão para a saída do console
    logging.basicConfig(level=logging_level, format="%(asctime)s %(levelname)s %(message)s")

    # 3. Processar Parâmetros de Conexão
    server_address = args.server # [9]
    cert = False # Argumento -cert foi omitido na AddArgs, usamos False.
    
    # Determinar URL do servidor [9]
    if server_address is None:
        server_address = f"{socket.getfqdn()}:{PORT}"
        server_url = f"https://{server_address}"
    else:
        server_url = server_address
        
    is_ksc_user = args.ksc_user # [9]
    user = args.user # [10]
    password = args.password # [10]
    
    # Solicitar senha se o usuário for fornecido mas a senha não [11]
    if user != None and password == None:
        password = getpass(prompt="Please input Password : ") # [11]

    # 4. Conectar ao Servidor
    server = ConnectServer(server_url, user, password, is_ksc_user, cert) # [11]
    
    if server is None:
        print("Falha na conexão com o servidor KSC. Verifique os logs.")
        return

    # 5. Lógica de Enumeração (Original de enumerating_all_groups.py)
    oHostGroup = KlAkHostGroup(server) # [3]

    # get id of root group ('Managed devices' group)
    nRootGroupID = oHostGroup.GroupIdGroups().RetVal() # [3]

    # enumerate subgroups of root group
    oSubgroups = oHostGroup.GetSubgroups(nRootGroupID, 0).RetVal() # [3]

    if oSubgroups == None or len(oSubgroups) == 0: # [3]
        print('Root group is empty')
    else:
        EnumerateGroups(oSubgroups, 0) # [3]


if __name__ == '__main__':
    main()