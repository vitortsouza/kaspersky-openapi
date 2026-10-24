import argparse

import urllib3

from KlAkOAPI.SrvView import KlAkSrvView
from KlAkOAPI.Error import KlAkError
from ksc_common import add_connection_args, connect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def listar_dispositivos(server):
    oSrvView = KlAkSrvView(server)

    wstrViewName = "UmdmDevices"
    wstrFilter = '(&(Dev_Model="*"))'
    vecFieldsToReturn = ["Dev_Id", "Dev_Model", "Dev_OS", "Dev_FrName", "Dev_PhNumber"]

    res_iterator = oSrvView.ResetIterator(
        wstrViewName,
        wstrFilter,
        vecFieldsToReturn,
        [],
        {},
        7200,
    )
    wstrIteratorId = res_iterator.OutPar("wstrIteratorId")

    iRecordCount = oSrvView.GetRecordCount(wstrIteratorId).RetVal()
    print(f"Total de dispositivos encontrados no KSC: {iRecordCount}")
    print("Buscando blocos de dispositivos cadastrados...")
    print("-" * 40)

    iStart = 0
    iStep = 100

    while iStart < iRecordCount:
        res_range = oSrvView.GetRecordRange(wstrIteratorId, iStart, iStep)
        pRecords = res_range.OutPar("pRecords")

        if pRecords is None:
            break

        try:
            records_array = pRecords["KLCSP_ITERATOR_ARRAY"]
        except (TypeError, KeyError):
            records_array = []

        if not records_array:
            break

        for idx, item in enumerate(records_array):
            print(f"Dispositivo {iStart + idx + 1}:")
            dev_id = item["Dev_Id"] if "Dev_Id" in item else "N/A"
            dev_name = item["Dev_FrName"] if "Dev_FrName" in item else "N/A"
            dev_model = item["Dev_Model"] if "Dev_Model" in item else "N/A"
            dev_os = item["Dev_OS"] if "Dev_OS" in item else "N/A"
            dev_phone = item["Dev_PhNumber"] if "Dev_PhNumber" in item else "N/A"

            print(f"\tID: {dev_id}")
            print(f"\tNome de Exibição: {dev_name}")
            print(f"\tModelo: {dev_model}")
            print(f"\tSistema Operacional: {dev_os}")
            print(f"\tTelefone: {dev_phone}")
            print("-" * 40)

        iStart += iStep

    oSrvView.ReleaseIterator(wstrIteratorId)
    print("\nListagem concluída com sucesso e recursos liberados.")


def main():
    parser = argparse.ArgumentParser(
        description="Lista dispositivos móveis cadastrados no KSC."
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
