import json
import asyncio

from exs_shell.state import State
from exs_shell.utils import Dirs
from exs_shell.interfaces.schemas.ipc.commands import Command
from exs_shell.interfaces.types import Commands

all_commands: Commands = State.commands


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
    group: str | None = None,
) -> None:
    if group in all_commands:
        help_text = (
            "\n".join(
                [
                    f"{name}: {cmd_obj.description}"
                    for name, cmd_obj in all_commands[group].items()
                ]
            )
            + "\n"
        )
    else:
        help_text = (
            "\n\n".join(
                [
                    f"{group}:\n\t{name}: {cmd_obj.description}"
                    for group, commands in all_commands.items()
                    for name, cmd_obj in commands.items()
                ]
            )
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
        cmd: list[str] = msg.get("cmd")
        if len(cmd) > 2:
            return await return_error(writer)
    except Exception:
        writer.close()
        return await writer.wait_closed()

    if cmd[0] in ["help", "-h", "--help"]:
        return await help_command(writer, cmd[1] if len(cmd) > 1 else None)

    command: Command | None = None
    group, name = cmd[0], cmd[1]
    if group in all_commands:
        command = all_commands.get(group, {}).get(name)

    if not command:
        return await return_error(writer)

    await run_command(writer, command)


async def run_ipc_server() -> None:
    server = await asyncio.start_unix_server(
        handle_client, path=f"{Dirs.TEMP_DIR}/ipc.sock"
    )
    async with server:
        await server.serve_forever()
