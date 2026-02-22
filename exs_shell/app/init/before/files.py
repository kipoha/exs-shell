from exs_shell.utils import Dirs


def init() -> None:
    Dirs.ensure_dirs_exist()
