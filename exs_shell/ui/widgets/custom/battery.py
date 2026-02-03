from ignis.services.upower import UPowerDevice

from exs_shell import register
from exs_shell.configs.user import user
from exs_shell.state import State
from exs_shell.ui.widgets.custom.circle import ArcMeter


@register.event
class Battery(ArcMeter):
    def __init__(
        self,
        size: int = 50,
        thickness: int = 7,
        arc_ratio: float = 0.75,
        speed: float = 0.15,
        label: str = "",
        show_percentage: bool = False,
        font_size: float = 20,
    ):
        self.battery: UPowerDevice = State.services.upower.batteries[0]
        self.icons: dict[str, str] = {
            "charging": "",
            "discharging": "",
            "full": "",
            "critical": "",
        }
        super().__init__(
            size, thickness, arc_ratio, speed, label, show_percentage, font_size
        )
        self._update()

    @register.events.battery("notify::percent")
    @register.events.battery("notify::charging")
    @register.events.battery("notify::charged")
    def _update(self, *_):
        perc = self.battery.get_property("percent")
        charged = bool(self.battery.get_property("charged"))
        charging = bool(self.battery.get_property("charging"))
        if charged:
            self.label = self.icons["full"]
        elif charging:
            self.label = self.icons["charging"]
        elif perc < user.critical_percentage:
            self.label = self.icons["critical"]
        else:
            self.label = self.icons["discharging"]
        self.set_value(perc / 100)
