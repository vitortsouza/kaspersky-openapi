#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
Este módulo gerencia tarefas do Kaspersky Security Center (KSC) via KlAkOAPI:
pesquisa por nome, exibe o último resultado e executa opcionalmente.
"""

import argparse
import socket
import logging
import time
from getpass import getpass
import json # Necessário para exibir o resultado JSON da GetTaskStatistics2
from pathlib import Path

# Importações KSC OAPI
from KlAkOAPI.AdmServer import KlAkAdmServer # Usado para conexão [1]
from KlAkOAPI.Tasks import KlAkTasks # Classe para gerenciar tarefas [1]
from KlAkOAPI.Params import KlAkArray, KlAkParams # Tipos de dados e containers [1]

# Importação para lidar com avisos de segurança
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # [6]

PORT = 13299 # Porta padrão do KSC [6]

# --- Funções Auxiliares de Conexão e Argumentos ---

def ConnectServer(server_url, username=None, password=None, ksc_user=False, cert=False):
    """Conecta ao servidor KSC principal usando as credenciais fornecidas."""
    try:
        server = KlAkAdmServer.Create(
            server_url, username, password, internal_user=ksc_user, verify=cert
        ) # [6, 7]
        logging.info("KSC server connection successfully!") # [6, 7]
        return server
    except Exception as e:
        logging.error(e) # [7, 8]
        return None

def AddArgs(parser):
    """Define os argumentos esperados na linha de comando."""
    group_address = parser.add_argument_group("Argumentos de Conexão e Autenticação") # [8]

    # Argumentos de Conexão
    group_address.add_argument("-server", action="store",
        help='(Opcional) Endereço onde o servidor KSC está localizado. Ex: "https://ksc.example.com:13299".') # [8, 9]
    group_address.add_argument("-user", action="store", help="Conta para autenticação no servidor KSC") # [10]
    group_address.add_argument("-password", action="store", help="Senha da conta para autenticação básica") # [10]
    group_address.add_argument("-ksc_user", action="store_true", help="Definir para conta interna do KSC") # [10]

    # Argumentos de Tarefa
    group_task = parser.add_argument_group("Argumentos de Tarefa") # [10]
    group_task.add_argument("-task", action="store", required=True, help='Nome da tarefa a ser pesquisada e exibir ultimo resultado.') # [10]
    group_task.add_argument("-run", action="store_true", help='(Opcional) Se definido, executa a tarefa após encontrá-la.') # [2]
    group_task.add_argument("-product_name", action="store", help='(Opcional) Nome do produto para filtrar a busca.') # [2]
    group_task.add_argument("-product_version", action="store", help='(Opcional) Versão do produto para filtrar a busca.') # [2]

    # Argumento de Debug
    group_address.add_argument("-d", action="store_true", help="Modo de log de debug") # [2, 11]
    return

# --- Funções Específicas de Gerenciamento de Tarefas ---

def FindTask(oTasks, strTaskName, strProductName='', strVersion=''):
    """
    Busca o ID da tarefa pelo nome de exibição (DisplayName) usando comparação
    case-insensitive, forçando o servidor a retornar todas as tarefas e
    filtrando localmente.
    """
    logging.info(f"Iniciando busca pela tarefa: '{strTaskName}' (Case-Insensitive)")

    # Prepara a string de busca em minúsculas
    target_name_lower = strTaskName.strip().lower()

    # Passamos strTaskName='' para forçar o KSC a retornar todas as tarefas,
    # caso o filtro rígido do servidor esteja falhando.
    try:
        iterator_id = oTasks.ResetTasksIterator(
            nGroupId=0,
            bGroupIdSignificant=False,
            strProductName=strProductName,
            strVersion=strVersion,
            strComponentName='', strInstanceId='',
            strTaskName='',  # <--- REMOVIDO O FILTRO DE NOME DA API AQUI
            bIncludeSupergroups=True
        ).OutPar('strTaskIteratorId')
    except Exception as e:
        logging.error(f"Falha ao iniciar o iterador de tarefas: {e}")
        return None, None

    task_id = None
    display_name = None

    while True:
        try:
            response = oTasks.GetNextTask(iterator_id)
            pTaskData = response.OutPar('pTaskData')

            if pTaskData is None or len(pTaskData) == 0:
                break

            current_task_dn = pTaskData.get('DisplayName', None)

            if current_task_dn is None and 'TASK_INFO_PARAMS' in pTaskData:
                 current_task_dn = pTaskData['TASK_INFO_PARAMS'].get('DisplayName')

            if current_task_dn:
                # Log de DEBUG que mostrará TODOS os nomes de tarefas
                logging.debug(f"Verificando Tarefa retornada: '{current_task_dn}'")

                # COMPARAÇÃO AGORA É CASE-INSENSITIVE
                if current_task_dn.strip().lower() == target_name_lower:
                    task_id = pTaskData.get('id', pTaskData.get('TASK_ID'))
                    if task_id is None:
                         task_id = pTaskData.get('strTask')

                    display_name = current_task_dn
                    break

        except Exception as e:
            logging.warning(f"Erro durante a iteração de tarefas: {e}")
            break

    # ... (Resto da função de limpeza e retorno) ...
    # Liberar o iterador
    try:
        oTasks.ReleaseTasksIterator(iterator_id)
    except Exception as e:
        logging.warning(f"Falha ao liberar iterador de tarefas: {e}")

    if task_id:
        logging.info(f"Tarefa encontrada. ID: {task_id}")
        return task_id, display_name
    else:
        logging.info(f"Tarefa '{strTaskName}' não encontrada.")
        return None, None


def GetTaskStatistics(oTasks, strTaskID):
    """Adquire e retorna as estatísticas da tarefa (último resultado) usando GetTaskStatistics2."""
    try:
        logging.info(f"Consultando estatísticas para a Tarefa ID: {strTaskID}") # [18]
        
        # GetTaskStatistics2 é o método recomendado (não obsoleto como GetTaskStatistics) [5, 19]
        response = oTasks.GetTaskStatistics2(strTaskID).respose_text # [19, 20]
        return response
    except Exception as e:
        logging.error(f"Falha ao obter estatísticas da tarefa: {e}") # [19]
        return {"Error": str(e)}

def RunTask(oTasks, strTaskID):
    """Inicia a execução da tarefa especificada. Utiliza Tasks.RunTask."""
    try:
        logging.info(f"Enviando comando de execução para a Tarefa ID: {strTaskID}") # [19]
        
        # RunTask inicia a tarefa. O retorno (retval) é geralmente False para sucesso [21, 22]
        oTasks.RunTask(strTaskID) # [21]
        
        print(f"\n--- EXECUÇÃO INICIADA ---")
        print(f"O comando para iniciar a tarefa ID {strTaskID} foi enviado com sucesso.") # [22]
        return True
    except Exception as e:
        # Erros do KSC são retornados no campo PxgError [23]
        logging.error(f"Falha ao iniciar a tarefa: {e}") # [22]
        print(f"\n--- ERRO NA EXECUÇÃO ---")
        print(f"Não foi possível iniciar a tarefa ID {strTaskID}. Verifique o log para detalhes.") # [22]
        return False

# --- Função Principal ---

def main():
    parser = argparse.ArgumentParser(description="Gerenciamento de Tarefas do KSC via KlAkOAPI") # [22]
    AddArgs(parser) # [24]
    args = parser.parse_args() # [24]

    # 1. Configurar Logging
    if args.d:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    
    logging.basicConfig(level=logging_level, format="%(asctime)s %(levelname)s %(message)s") # [24]

    # 2. Processar Parâmetros de Conexão
    server_address = args.server
    cert = False
    
    if server_address is None:
        server_address = f"{socket.getfqdn()}:{PORT}"
        server_url = f"https://{server_address}"
    else:
        server_url = server_address # [24]

    is_ksc_user = args.ksc_user # [25]
    user = args.user # [25]
    password = args.password # [25]
    
    if user is not None and password is None:
        password = getpass(prompt="Please input Password : ") # [25, 26]

    # 3. Conectar ao Servidor
    server = ConnectServer(server_url, user, password, is_ksc_user, cert) # [25]
    if server is None:
        print("Falha na conexão com o servidor KSC. Verifique os logs.") # [25]
        return

    # 4. Lógica de Tarefa
    task_name = args.task
    should_run = args.run
    product_name = args.product_name if args.product_name else ""
    product_version = args.product_version if args.product_version else ""
    
    print(f"\n**Sucesso na Conexão e Parsing de Argumentos.**") # [3]
    print(f"Servidor: {server_url}")
    print(f"Tarefa Solicitada: {task_name}")
    if product_name:
         print(f"Filtro de Produto: {product_name} ({product_version})") # [3]
    print(f"Instrução: A tarefa deve ser {'EXECUTADA' if should_run else 'APENAS PESQUISADA'} após a pesquisa.") # [3]

    # 4.1 Instanciar a classe de Tarefas
    oTasks = KlAkTasks(server) # [3]

    # 4.2 Encontrar a tarefa pelo nome 
    task_id, found_name = FindTask(oTasks, task_name, product_name, product_version) # [3]
    
    if task_id is None:
        print(f"\nERRO: Tarefa '{task_name}' não foi localizada no KSC.") # [27]
        return

    # 4.3 Consultar e exibir o último resultado/estatísticas
    statistics = GetTaskStatistics(oTasks, task_id) # [27]

    print(f"\n--- ESTATÍSTICAS/ÚLTIMO RESULTADO DA TAREFA ({found_name}) ---")
    if statistics and 'Error' not in statistics:
        # Exibir JSON formatado, pois as respostas KSC são JSON [23, 28]
        print(json.dumps(statistics, indent=4)) # [27]
    else:
        print("Não foi possível recuperar as estatísticas da tarefa ou ocorreu um erro.") # [29]
        if 'Error' in statistics:
             print(f"Detalhes do erro: {statistics['Error']}") # [29]

    # 4.4 Executar a tarefa, se solicitado
    if should_run:
        RunTask(oTasks, task_id) # [29]

if __name__ == '__main__':
    main()