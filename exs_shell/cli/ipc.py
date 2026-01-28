import sys
import asyncio

from loguru import logger

from exs_shell.app.vars import APP_NAME
from exs_shell.controllers.ipc.client import send_command


def main():
    if len(sys.argv) < 2:
        logger.error("Usage: exs-ipc <command>")
        exit(1)
    try:
        asyncio.run(send_command(sys.argv[1]))
    except ConnectionRefusedError:
        logger.error(f"{APP_NAME} IPC is not running")
        exit(1)


if __name__ == "__main__":
    main()
