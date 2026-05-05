from libexs.utils import run_async_task
from exs_shell.controllers.ipc.server import run_ipc_server


def init() -> None:
    run_async_task(run_ipc_server())
