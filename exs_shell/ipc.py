import sys
import asyncio

from exs_shell.ipc_utils.client import send_command


def main():
    if len(sys.argv) < 2:
        print("Usage: python ipc.py <command>")
        exit(1)
    try:
        asyncio.run(send_command(sys.argv[1]))
    except ConnectionRefusedError:
        print("Shell is not running")
        exit(1)


if __name__ == "__main__":
    main()
