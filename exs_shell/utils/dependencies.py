from typing import cast

from ignis.utils import exec_sh
from ignis.services.niri import NiriService

from exs_shell.state import State


def check_lock() -> bool:
    data = exec_sh("which exs-lock")
    return data.returncode == 0


def niri_active() -> bool:
    service = cast(NiriService | None, State.services.get("niri"))
    return bool(service and service.is_available)
