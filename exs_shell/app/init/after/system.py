from pathlib import Path
from libexs.utils import run_async_task
from exs_shell.configs.user import user
from exs_shell.controllers.ipc.server import run_ipc_server


def init() -> None:
    Path(user.plugins_dir).mkdir(parents=True, exist_ok=True)
    run_async_task(run_ipc_server())
