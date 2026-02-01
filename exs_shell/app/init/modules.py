from exs_shell.utils.loop import run_async_task
from exs_shell.controllers.ipc.server import run_ipc_server
from exs_shell.ui.modules.settings.widget import Settings
from exs_shell.ui.modules.bar.widget import init_bars


def init() -> None:
    run_async_task(run_ipc_server())
    Settings()
    init_bars()
