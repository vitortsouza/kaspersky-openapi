# KlAkOAPI

Utilitários de linha de comando para administrar o Kaspersky Security Center (KSC) usando a API `KlAkOAPI`.

## Aviso de segurança

Este repositório não contém servidores, usuários ou senhas reais. Os exemplos usam valores genéricos como `ksc.exemplo.com` e `api-user`.

Nunca grave credenciais em arquivos versionados. Prefira variáveis de ambiente ou o prompt interativo de senha.

## Requisitos

- Windows para os wrappers `.cmd` e para os recursos de AD (`pywin32`).
- Python 3.10 ou superior. O utilitário `add_category.py` usa `match`.
- Acesso de rede ao servidor KSC na porta da API (normalmente `13299`).

## Instalação

```bat
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

O pacote vendorizado `KlAkOAPI-1.0.0.0` é instalado em modo editável pelo `requirements.txt`.

## Configuração

Os scripts que usam `ksc_common.py` aceitam argumentos ou variáveis de ambiente:

| Variável | Descrição |
| --- | --- |
| `KSC_SERVER` | URL do KSC, por exemplo `https://ksc.exemplo.com:13299` |
| `KSC_USER` | Usuário da API |
| `KSC_PASSWORD` | Senha. Se omitida, será solicitada |
| `KSC_USER_INTERNAL` | `1` para conta interna do KSC |
| `KSC_DOMAIN` | Domínio AD, quando aplicável |
| `KSC_CERT` | Caminho do certificado CA do servidor |
| `KSC_VERIFY` | `1` para habilitar a verificação SSL |

Exemplo no `cmd.exe`:

```bat
set KSC_SERVER=https://ksc.exemplo.com:13299
set KSC_USER=api-user
set KSC_USER_INTERNAL=1
py list_all_devices.py
```

A senha pode ser informada com `-password`, mas isso pode deixá-la no histórico do shell. O padrão é solicitar a senha no terminal.

## Utilitários

| Script | Função |
| --- | --- |
| `list_all_devices.py` | Lista computadores e servidores cadastrados |
| `list_mobile_devices.py` | Lista dispositivos móveis |
| `find_task.py` | Localiza e executa uma tarefa pelo nome |
| `add_category_app_control/add_category.py` | Importa hashes SHA-256 para uma categoria de IoC |
| `add_internal_user/add_internal_user.py` | Cria um usuário interno no KSC |
| `create_remove_search_groups/create_remove_search_groups.py` | Enumera, pesquisa, adiciona e remove grupos; integra OUs do AD |
| `enumerating_all_groups/enumerating_all_groups.py` | Enumera grupos do KSC |
| `enumerating_tasks_querying_task_running_task/enumerating_tasks_querying_task_running_task.py` | Enumera tarefas e consulta/executa uma tarefa |
| `find_run_task/find_run_task.py` | Lista, localiza, consulta o status e executa tarefas |

## Exemplos

```bat
py list_all_devices.py -server https://ksc.exemplo.com:13299 -user api-user -ksc_user
py list_mobile_devices.py -server https://ksc.exemplo.com:13299 -user api-user -ksc_user
py find_task.py -server https://ksc.exemplo.com:13299 -user api-user -ksc_user -task "Optimized Full Scan - KES"
```

Para usar uma conta de domínio:

```bat
py list_all_devices.py -server https://ksc.exemplo.com:13299 -user joao -domain EMPRESA
```

Para validar o certificado do servidor:

```bat
py list_all_devices.py -server https://ksc.exemplo.com:13299 -user api-user -ksc_user -cert C:\caminho\ca.pem
```

## Wrappers `.cmd`

Cada pasta possui um `.cmd` que solicita servidor e usuário e deixa o Python pedir a senha. Também é possível definir `KSC_SERVER`, `KSC_USER`, `KSC_PASSWORD` e outras variáveis antes de executar. Os wrappers também aceitam `KSC_NEW_USER`, `KSC_CATEGORY` e `KSC_TASK`.

Exemplos:

```bat
add_category_app_control\add_category.cmd
add_internal_user\add_internal_user.cmd
create_remove_search_groups\create_remove_search_groups.cmd -e
find_run_task\find_run_task.cmd
```

## SSL

Os utilitários mantêm compatibilidade com servidores que usam certificado autoassinado. Quando o script aceitar `-cert` ou `-verify`, prefira validar o certificado:

- `-cert caminho\ca.pem`: valida usando o certificado informado.
- `-verify`: valida usando os certificados do sistema.

Sem essas opções, a verificação SSL fica desabilitada, como nos scripts originais.

## Estrutura

- `KlAkOAPI-1.0.0.0/`: pacote vendorizado da API. Os samples internos usam credenciais fictícias (`klakoapi_test` / `test1234!`) e não devem ser usados como configuração real.
- `ksc_common.py`: argumentos e conexão compartilhados pelos utilitários principais.
- `KSC_OpenApi sample1.pdf` e `KSC_OpenApi sample2.pdf`: documentação de referência da API.

## Observações

- `create_remove_search_groups.py` depende de `pywin32` e de um ambiente Windows para os recursos de AD.
- `find_task.py` executa a tarefa encontrada. Para apenas listar, consultar status ou executar com mais controle, use `find_run_task.py`.
- Logs, ambientes virtuais, caches e arquivos de configuração local estão no `.gitignore`.
