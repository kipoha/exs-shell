import time
import subprocess

from gi.repository import GLib  # type: ignore

from ignis.base_service import BaseService
from ignis.utils import exec_sh_async

from exs_shell import register
from exs_shell.configs.user import user
from exs_shell.utils.loop import run_async_task


@register.event
class IdleService(BaseService):
    def __init__(self):
        super().__init__()
        self.actions = user.get_idle_actions_objs()
        self._executed = [False] * len(self.actions)
        self._is_idle = False
        self._last_event = time.time()
        self._timer_interval = 1

        self._proc = None
        self._listen_event_stream()
        GLib.timeout_add_seconds(self._timer_interval, self._check_idle)

    def _listen_event_stream(self):
        self._proc = subprocess.Popen(
            ["niri", "msg", "event-stream"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        GLib.io_add_watch(self._proc.stdout.fileno(), GLib.IO_IN, self._on_event_line)  # type: ignore

    @register.events.option(user, "idle_actions")
    def __update(self, *_):
        self.actions = user.get_idle_actions_objs()
        self._executed = [False] * len(self.actions)

    def _on_event_line(self, fd, condition):
        line = self._proc.stdout.readline()  # type: ignore
        if line.strip():
            self._last_event = time.time()
        return True

    def _check_idle(self):
        now = time.time()
        idle_seconds = now - self._last_event

        if idle_seconds < 1:
            if self._is_idle:
                for i, action in enumerate(self.actions):
                    if self._executed[i]:
                        if action.on_resume:
                            run_async_task(exec_sh_async(action.on_resume))
                self._is_idle = False
                self._executed = [False] * len(self.actions)
        else:
            if not self._is_idle:
                self._is_idle = True

            for i, action in enumerate(self.actions):
                if not self._executed[i] and idle_seconds >= action.timeout_seconds:
                    run_async_task(exec_sh_async(action.on_timeout))
                    self._executed[i] = True

        return True
