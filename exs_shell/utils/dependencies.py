from ignis.utils import exec_sh


def check_lock() -> bool:
    data = exec_sh("which exs-lock")
    if data.returncode == 0:
        return True
    return False
