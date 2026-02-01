import os
import sys

from loguru import logger

from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler

from exs_shell.utils.path import Paths

IGNORE_PATHS = (".venv", "__pycache__", ".git", "node_modules", "pg_storage")


class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        if not event.src_path.endswith(".py"):  # type: ignore
            return

        for ignore in IGNORE_PATHS:
            if ignore in event.src_path:  # type: ignore
                return

        logger.debug(f"File changed: {event.src_path}, restarting...")

        root = str(Paths.root)
        os.chdir(root)
        os.environ["PYTHONPATH"] = root

        python = sys.executable
        os.execv(python, [python, "-m", "exs_shell.cli.shell"] + sys.argv[1:])
