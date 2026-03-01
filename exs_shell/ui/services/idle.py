import time
import subprocess

from gi.repository import GLib  # type: ignore

from loguru import logger

from ignis.base_service import BaseService
from ignis.utils import exec_sh_async

from exs_shell import register
from exs_shell.configs.user import user
from exs_shell.utils.loop import run_async_task
from exs_shell.utils.path import Paths


@register.event
class IdleService(BaseService):
    def __init__(self):
        super().__init__()
        self.actions = user.get_idle_actions_objs()
        self._executed = [False] * len(self.actions)
        self._is_idle = False
        self._idle_start = None
        self._stdout_watch = None
        self._stderr_watch = None
        self._timeout_id = None

        self._proc = None
        self._enabled = False

        if user.idle_enable:
            self.enable()

    def _start_idle_binary(self):
        logger.info("START IDLE")
        idle_binary = str(Paths.path / "extensions/idle/wl_idle_helper")
        self._proc = subprocess.Popen(
            [idle_binary, "2000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._child_watch = GLib.child_watch_add(self._proc.pid, self._on_process_exit)
        logger.info("IDLE STARTED")

        self._stdout_watch = GLib.io_add_watch(
            self._proc.stdout.fileno(),  # type: ignore
            GLib.IO_IN,
            self._on_idle_stdout,
        )
        self._stderr_watch = GLib.io_add_watch(
            self._proc.stderr.fileno(),  # type: ignore
            GLib.IO_IN,
            self._on_idle_stderr,
        )
        logger.info("IDLE WATCHERS ADDED")

    @register.events.option(user, "idle_actions")
    def __update(self, *_):
        self.actions = user.get_idle_actions_objs()
        self._executed = [False] * len(self.actions)

    @register.events.option(user, "idle_enable")
    def __toggle_idle(self, *_):
        if user.idle_enable:
            self.enable()
        else:
            self.disable()

    def _on_idle_stdout(self, fd, condition):
        if not self._proc or not self._proc.stdout:
            return False
        line = self._proc.stdout.readline()
        if not line:
            return True

        line = line.strip()
        if not line:
            return True
        logger.info(f"IDLE: {line}")

        if line == "idle":
            if not self._is_idle:
                self._is_idle = True
                self._idle_start = time.time()
        elif line == "resume":
            if self._is_idle:
                self._is_idle = False
                self._idle_start = None
                for i, action in enumerate(self.actions):
                    if self._executed[i] and action.on_resume:
                        logger.info(f'executing resume action "{action.on_resume}"')
                        run_async_task(exec_sh_async(action.on_resume))
                self._executed = [False] * len(self.actions)
        else:
            self._is_idle = False
            self._idle_start = None
            self._executed = [False] * len(self.actions)

        return True

    def _on_idle_stderr(self, fd, condition):
        if not self._proc or not self._proc.stderr:
            return False
        line = self._proc.stderr.readline()
        if line:
            logger.error(f"wl_idle_helper stderr: {line.strip()}")
        return True

    def _check_idle(self):
        if not self._enabled:
            return True
        if self._is_idle and self._idle_start is not None:
            now = time.time()
            idle_seconds = now - self._idle_start
            logger.info(f"idle seconds: {idle_seconds}")
            for i, action in enumerate(self.actions):
                if not self._executed[i] and idle_seconds >= action.timeout_seconds:
                    logger.info(f'executing idle action "{action.on_timeout}"')
                    run_async_task(exec_sh_async(action.on_timeout))
                    self._executed[i] = True
        return True

    def _reset_state(self):
        self._is_idle = False
        self._idle_start = None
        self._executed = [False] * len(self.actions)

    def enable(self):
        if self._enabled:
            return

        logger.info("IdleService ENABLE")

        self._enabled = True
        self._reset_state()
        self._start_idle_binary()

        if self._timeout_id is None:
            self._timeout_id = GLib.timeout_add_seconds(1, self._check_idle)

    def disable(self):
        if not self._enabled:
            return

        logger.info("IdleService DISABLE")

        self._enabled = False
        self._reset_state()

        if self._proc:
            self._proc.terminate()
            self._proc.wait(timeout=1)
            self._proc = None

        if self._stdout_watch:
            GLib.source_remove(self._stdout_watch)
            self._stdout_watch = None

        if self._stderr_watch:
            GLib.source_remove(self._stderr_watch)
            self._stderr_watch = None

        if self._timeout_id:
            GLib.source_remove(self._timeout_id)
            self._timeout_id = None

    def _on_process_exit(self, pid, status):
        logger.info(f"wl_idle_helper exited with status {status}")

        if self._proc:
            try:
                self._proc.wait(timeout=0)
            except Exception:
                pass

        self._proc = None
        return False
