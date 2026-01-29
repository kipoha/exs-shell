import sys
import asyncio
import traceback

from loguru import logger

from exs_shell.app.vars import APP_NAME
from exs_shell.controllers.ipc.client import send_command


def main():
    if len(sys.argv) < 2:
        logger.error("Usage: exs-ipc <command>")
        exit(1)
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_command(sys.argv[1]))
    except ConnectionRefusedError:
        logger.error(f"{APP_NAME} IPC is not running")
        exit(1)
    except Exception:
        e = traceback.format_exc()
        logger.error(e)
        exit(1)


if __name__ == "__main__":
    main()
