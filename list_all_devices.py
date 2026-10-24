import argparse

import urllib3

from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.ChunkAccessor import KlAkChunkAccessor
from KlAkOAPI.Error import KlAkError
from ksc_common import add_connection_args, connect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def listar_dispositivos(server):
    oHostGroup = KlAkHostGroup(server)
    oChunkAccessor = KlAkChunkAccessor(server)

    wstrFilter = '(&(KLHST_WKS_HOSTNAME="*"))'
    vecFieldsToReturn = [
        "KLHST_WKS_DN",
        "KLHST_WKS_HOSTNAME",
        "KLHST_WKS_IP_LONG",
        "KLHST_WKS_DNSNAME",
    ]
    pParams = {"KLGRP_FIND_FROM_CUR_VS_ONLY": True}

    host_info = oHostGroup.FindHosts(
        wstrFilter, vecFieldsToReturn, [], pParams, 3600
    )
    strAccessor = host_info.OutPar("strAccessor")

    nCount = oChunkAccessor.GetItemsCount(strAccessor).RetVal()
    print(f"Total de computadores/servidores encontrados no KSC: {nCount}")
    print("Buscando blocos de dispositivos cadastrados...")
    print("-" * 40)

    nStart = 0
    nStep = 100

    while nStart < nCount:
        oChunk = oChunkAccessor.GetItemsChunk(strAccessor, nStart, nStep)
        pChunk = oChunk.OutPar("pChunk")

        records_array = []
        if pChunk is not None:
            try:
                records_array = pChunk["KLCSP_ITERATOR_ARRAY"]
            except (TypeError, KeyError):
                pass

        if not records_array:
            break

        for idx, item in enumerate(records_array):
            print(f"Dispositivo {nStart + idx + 1}:")
            dev_name = item["KLHST_WKS_DN"] if "KLHST_WKS_DN" in item else "N/A"
            dev_id = (
                item["KLHST_WKS_HOSTNAME"]
                if "KLHST_WKS_HOSTNAME" in item
                else "N/A"
            )
            dev_ip = (
                item["KLHST_WKS_IP_LONG"]
                if "KLHST_WKS_IP_LONG" in item
                else "N/A"
            )
            dev_dns = (
                item["KLHST_WKS_DNSNAME"]
                if "KLHST_WKS_DNSNAME" in item
                else "N/A"
            )

            print(f"\tNome de Exibição: {dev_name}")
            print(f"\tID Exclusivo: {dev_id}")
            print(f"\tNome DNS: {dev_dns}")
            print(f"\tIP (Raw/Long): {dev_ip}")
            print("-" * 40)

        nStart += nStep

    oChunkAccessor.Release(strAccessor)
    print("\nListagem de computadores concluída com sucesso e recursos liberados.")


def main():
    parser = argparse.ArgumentParser(
        description="Lista computadores e servidores cadastrados no KSC."
    )
    add_connection_args(parser)
    args = parser.parse_args()

    try:
        server = connect(args)
        listar_dispositivos(server)
    except KlAkError as e:
        print(f"Erro na API do KSC (KlAkError): {e.data}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    main()
