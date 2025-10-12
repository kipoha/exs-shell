import json
import asyncio
from typing import Any
from utils import Dirs


async def return_error(writer: asyncio.StreamWriter) -> None:
    writer.write(b"error: unknown command\n")
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def run_command(
    writer: asyncio.StreamWriter, cmd_obj: tuple[object, str, dict[str, Any], str]
) -> None:
    obj, attr, kwargs, _ = cmd_obj

    getattr(obj, attr)(**kwargs)

    writer.write(b"ok\n")
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def help_command(
    writer: asyncio.StreamWriter,
    commands: dict[str, tuple[object, str, dict[str, Any], str]],
) -> None:
    help_data = {name: cmd_obj[3] for name, cmd_obj in commands.items()}

    help_text = (
        "\n".join([f"{name}: {description}" for name, description in help_data.items()])
        + "\n"
    )
    writer.write(help_text.encode("utf-8"))
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def handle_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    from ipc_utils.utils import commands

    data = await reader.readline()
    if not data:
        writer.close()
        await writer.wait_closed()
        return

    try:
        msg = json.loads(data.decode())
        cmd = msg.get("cmd")
    except Exception:
        writer.close()
        await writer.wait_closed()
        return

    if cmd == "help":
        await help_command(writer, commands)
        return

    command = commands.get(cmd)
    if not command:
        await return_error(writer)
        return

    await run_command(writer, command)


async def run_ipc_server() -> None:
    server = await asyncio.start_unix_server(handle_client, path=f"{Dirs.TEMP_DIR}/ipc.sock")
    async with server:
        await server.serve_forever()
