import json
import asyncio

from exs_shell.utils import Dirs
from exs_shell.controllers.commands import include_commands
from exs_shell.interfaces.schemas.ipc.commands import Command
from exs_shell.interfaces.types import Commands


async def return_error(writer: asyncio.StreamWriter) -> None:
    writer.write(b"error: unknown command\n")
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def run_command(writer: asyncio.StreamWriter, cmd: Command) -> None:
    cmd.call(*cmd.args, **cmd.kwargs)
    writer.write(b"ok\n")
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def help_command(
    writer: asyncio.StreamWriter,
    commands: Commands,
) -> None:
    help_data = {name: cmd_obj.description for name, cmd_obj in commands.items()}

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
    data = await reader.readline()
    if not data:
        writer.close()
        return await writer.wait_closed()

    try:
        msg = json.loads(data.decode())
        cmd = msg.get("cmd")
    except Exception:
        writer.close()
        return await writer.wait_closed()

    commands = include_commands()
    if cmd == "help":
        return await help_command(writer, commands)

    command = commands.get(cmd)
    if not command:
        return await return_error(writer)

    await run_command(writer, command)


async def run_ipc_server() -> None:
    server = await asyncio.start_unix_server(
        handle_client, path=f"{Dirs.TEMP_DIR}/ipc.sock"
    )
    async with server:
        await server.serve_forever()
