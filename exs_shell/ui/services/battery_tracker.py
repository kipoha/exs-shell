from typing import Any

from ignis.base_service import BaseService

from exs_shell import register
from exs_shell.configs.user import user
from exs_shell.state import State
from exs_shell.utils.notify_system import send_notification


@register.event
class BatteryTrackerService(BaseService):
    def __init__(self):
        super().__init__()
        self.battery = State.services.upower.batteries[0]
        self._notified_low = False
        self.__track()

    @register.events.battery("notify::percent")
    @register.events.battery("notify::charging")
    @register.events.battery("notify::charged")
    def __track(self, *_: Any) -> None:
        percent: float = self.battery.get_property("percent")
        charged = bool(self.battery.get_property("charged"))
        charging = bool(self.battery.get_property("charging"))

        if charged or charging or percent >= user.critical_percentage:
            self._notified_low = False
            return

        if percent < user.critical_percentage and not self._notified_low:
            send_notification("Low battery", f"{percent}%")
            self._notified_low = True
