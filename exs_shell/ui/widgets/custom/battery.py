from ignis.services.upower import UPowerDevice, UPowerService

from exs_shell import register
from exs_shell.state import State
from exs_shell.ui.widgets.custom.circle import ArcMeter


@register.event
class Battery(ArcMeter):
    def __init__(
        self,
        size: int = 60,
        thickness: int = 10,
        arc_ratio: float = 0.75,
        speed: float = 0.15,
        label: str = "",
    ):
        self.battery: UPowerDevice = State.services.upower.batteries[0]
        self.icons = {
            "charging": "",
            "discharging": "",
            "full": "",
        }
        super().__init__(size, thickness, arc_ratio, speed, label, True)
        # self._update()

    @register.events.battery("notify::percent")
    def percent(self, *_):
        self._update()

    @register.events.battery("notify::charging")
    def charging(self, *_):
        self._update()

    @register.events.battery("notify::charged")
    def charged(self, *_):
        self._update()

    def _update(self, *_):
        print("AKJSDKJDKSJDk")
        perc = self.battery.get_property("percent")
        self.set_value(perc / 100)
        charged = bool(self.battery.get_property("charged"))
        charging = bool(self.battery.get_property("charging"))
        if charged:
            self.label = self.icons["full"]
        elif charging:
            self.label = self.icons["charging"]
        else:
            self.label = self.icons["discharging"]
