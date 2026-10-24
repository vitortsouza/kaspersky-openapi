import argparse
import getpass
import os

from KlAkOAPI.AdmServer import KlAkAdmServer


def _env_flag(name):
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes", "sim")


def add_connection_args(parser):
    parser.add_argument(
        "-server",
        default=os.getenv("KSC_SERVER"),
        required=not bool(os.getenv("KSC_SERVER")),
        help="URL do KSC, por exemplo: https://ksc.example.com:13299",
    )
    parser.add_argument(
        "-user",
        default=os.getenv("KSC_USER"),
        required=not bool(os.getenv("KSC_USER")),
        help="Usuario para autenticacao no KSC",
    )
    parser.add_argument(
        "-password",
        default=os.getenv("KSC_PASSWORD"),
        help="Senha do KSC. Se omitida, sera solicitada.",
    )
    parser.add_argument(
        "-ksc_user",
        action="store_true",
        default=_env_flag("KSC_USER_INTERNAL"),
        help="Indica que a conta e interna do KSC",
    )
    parser.add_argument(
        "-domain",
        default=os.getenv("KSC_DOMAIN", ""),
        help="Dominio AD, quando aplicavel",
    )
    parser.add_argument(
        "-cert",
        default=os.getenv("KSC_CERT"),
        help="Caminho do certificado CA do servidor",
    )
    parser.add_argument(
        "-verify",
        action="store_true",
        default=_env_flag("KSC_VERIFY"),
        help="Habilita a verificacao SSL",
    )


def connect(args):
    username = args.user
    if not args.ksc_user and args.domain:
        username = f"{args.domain}\\{args.user}"

    password = args.password
    if password is None:
        password = getpass.getpass("Senha do KSC: ")

    verify = args.cert if args.cert else args.verify
    return KlAkAdmServer.Create(args.server, username, password, verify=verify)
