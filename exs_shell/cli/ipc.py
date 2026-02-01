import sys
import traceback

from loguru import logger

from exs_shell.app.vars import APP_NAME
from exs_shell.controllers.ipc.client import send_command
from exs_shell.utils.loop import run_async


def main():
    if len(sys.argv) < 2:
        logger.error("Usage: exs-ipc <command>")
        exit(1)
    try:
        run_async(send_command(sys.argv[1]))
    except ConnectionRefusedError:
        logger.error(f"{APP_NAME} IPC is not running")
        exit(1)
    except Exception:
        e = traceback.format_exc()
        logger.error(e)
        exit(1)


if __name__ == "__main__":
    main()
