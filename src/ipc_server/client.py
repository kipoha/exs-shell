import asyncio
import json


async def send_command(cmd: str):
    reader, writer = await asyncio.open_unix_connection("/tmp/exs-shell.sock")
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
