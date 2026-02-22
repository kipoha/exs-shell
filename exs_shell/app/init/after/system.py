from exs_shell.controllers.ipc.server import run_ipc_server
from exs_shell.utils.loop import run_async_task


def init() -> None:
    run_async_task(run_ipc_server())
