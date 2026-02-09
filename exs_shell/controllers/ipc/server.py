import json
import asyncio

from exs_shell.state import State
from exs_shell.utils import Dirs
from exs_shell.interfaces.schemas.ipc.commands import Command
from exs_shell.interfaces.types import Commands

all_commands: Commands = State.commands


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
        help_text = ""
        for group, commands in all_commands.items():
            help_text += f"{group}:\n"
            for name, cmd_obj in commands.items():
                help_text += f"\t{name}: {cmd_obj.description}\n"
            help_text += "\n"
    writer.write(help_text.encode("utf-8"))
    await writer.drain()
    writer.close()


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        data = await reader.read(4096)
        if not data:
            writer.close()
            return

        msg = json.loads(data.decode())
        cmd: list[str] = msg.get("cmd")
        if len(cmd) > 2:
            writer.write(b"error: unknown command\n")
            await writer.drain()
            writer.close()
            return

        if cmd[0] in ["help", "-h", "--help"]:
            await help_command(writer, cmd[1] if len(cmd) > 1 else None)
            return

        group, name = cmd[0], cmd[1]
        command: Command | None = all_commands.get(group, {}).get(name)
        if not command:
            writer.write(b"error: unknown command\n")
            await writer.drain()
            writer.close()
            return

        command.call(*command.args, **command.kwargs)

        writer.write(b"ok\n")
        await writer.drain()

    except ConnectionResetError:
        pass
    except Exception:
        writer.write(b"error\n")
        await writer.drain()
    finally:
        writer.close()


async def run_ipc_server() -> None:
    server = await asyncio.start_unix_server(
        handle_client, path=f"{Dirs.TEMP_DIR}/ipc.sock"
    )
    async with server:
        await server.serve_forever()
