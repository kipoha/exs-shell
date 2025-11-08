import asyncio
import json

from exs_shell.utils import Dirs


async def send_command(cmd: str):
    reader, writer = await asyncio.open_unix_connection(f"{Dirs.TEMP_DIR}/ipc.sock")
    writer.write(json.dumps({"cmd": cmd}).encode() + b"\n")
    await writer.drain()

    response = b""
    while True:
        line = await reader.readline()
        if not line:
            break
        response += line

    print(response.decode("utf-8"))

    writer.close()
    await writer.wait_closed()
