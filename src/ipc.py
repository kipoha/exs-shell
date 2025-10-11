import sys
import asyncio

from ipc_server.client import send_command


def main():
    if len(sys.argv) < 2:
        print("Usage: python ipc.py <command>")
        exit(1)
    asyncio.run(send_command(sys.argv[1]))


if __name__ == "__main__":
    main()
