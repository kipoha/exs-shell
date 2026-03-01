import time
import subprocess

from gi.repository import GLib  # type: ignore

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

        self._proc = None
        self._start_idle_binary()

        GLib.timeout_add_seconds(1, self._check_idle)

    def _start_idle_binary(self):
        idle_binary = str(Paths.path / "extensions/idle/wl_idle_helper")
        self._proc = subprocess.Popen(
            [idle_binary, "2000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        GLib.io_add_watch(self._proc.stdout.fileno(), GLib.IO_IN, self._on_idle_stdout)  # type: ignore
        GLib.io_add_watch(self._proc.stderr.fileno(), GLib.IO_IN, self._on_idle_stderr)  # type: ignore

    @register.events.option(user, "idle_actions")
    def __update(self, *_):
        self.actions = user.get_idle_actions_objs()
        self._executed = [False] * len(self.actions)

    def _on_idle_stdout(self, fd, condition):
        line = self._proc.stdout.readline()  # type: ignore
        if not line:
            return True

        line = line.strip()
        if not line:
            return True

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
                        run_async_task(exec_sh_async(action.on_resume))
                self._executed = [False] * len(self.actions)
        else:
            self._is_idle = False
            self._idle_start = None
            self._executed = [False] * len(self.actions)

        return True

    def _on_idle_stderr(self, fd, condition):
        line = self._proc.stderr.readline()  # type: ignore
        if line:
            print("wl_idle_helper stderr:", line.strip())
        return True

    def _check_idle(self):
        if self._is_idle and self._idle_start is not None:
            print("IDLE:", self._is_idle)
            print("IDLE seconds:", time.time() - self._idle_start)
            now = time.time()
            idle_seconds = now - self._idle_start
            for i, action in enumerate(self.actions):
                if not self._executed[i] and idle_seconds >= action.timeout_seconds:
                    run_async_task(exec_sh_async(action.on_timeout))
                    self._executed[i] = True
        return True
