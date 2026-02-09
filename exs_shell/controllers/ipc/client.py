import json
import asyncio

from exs_shell.utils import Dirs


async def send_command(*cmd: str) -> None:
    reader, writer = await asyncio.open_unix_connection(f"{Dirs.TEMP_DIR}/ipc.sock")
    writer.write(json.dumps({"cmd": cmd}).encode() + b"\n")
    await writer.drain()

    response = await reader.read(4096)
    print(response.decode("utf-8"))

    writer.close()
