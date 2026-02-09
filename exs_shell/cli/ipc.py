import argparse
import traceback

from loguru import logger

from exs_shell.app.vars import APP_NAME
from exs_shell.controllers.ipc.client import send_command
from exs_shell.utils.loop import run_async


def ipc_cmd(parser: argparse.ArgumentParser):
    parser.add_argument("group", nargs="?", default="-h", help="Command group")
    parser.add_argument("action", nargs="?", default=None, help="Command action")
    parser.set_defaults(func=run_ipc)


def run_ipc(args: argparse.Namespace):
    try:
        run_async(send_command(args.group, args.action))
    except ConnectionRefusedError:
        logger.error(f"{APP_NAME} IPC is not running")
        exit(1)
    except Exception:
        e = traceback.format_exc()
        logger.error(e)
        exit(1)
