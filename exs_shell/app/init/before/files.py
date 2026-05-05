from exs_shell.app.path import Dirs


def init() -> None:
    Dirs.ensure_dirs_exist()
