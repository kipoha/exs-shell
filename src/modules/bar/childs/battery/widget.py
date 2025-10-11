from ignis import widgets
from ignis.services.upower import UPowerService

from config.user import options

battery_cfg = options.user_config.battery


class Battery(widgets.Label):
    def __init__(self):
        super().__init__(
            label=battery_cfg.get("format", "{icon} {percentage}%").format(
                icon="", percentage="--"
            )
        )
        self.upower = UPowerService.get_default()

        batteries = self.upower.batteries
        if not batteries:
            return

        self.battery = batteries[0]

        self.battery.connect("notify::percent", lambda *_: self._update_label())
        self.battery.connect("notify::charging", lambda *_: self._update_label())
        self.battery.connect("notify::charged", lambda *_: self._update_label())

        self._update_label()

    def _update_label(self):
        perc = self.battery.get_property("percent") or 0
        charging = bool(
            self.battery.get_property("charging")
            or self.battery.get_property("charged")
        )

        icons_cfg = battery_cfg.get("icons", {})
        icon = ""

        if perc >= 100:
            icon = icons_cfg.get("100", "")
        elif perc >= 70:
            icon = icons_cfg.get("70", "")
        elif perc >= 50:
            icon = icons_cfg.get("50", "")
        elif perc >= 30:
            icon = icons_cfg.get("30", "")
        else:
            icon = icons_cfg.get("10", "")

        if perc <= battery_cfg.get("critical_level", 10):
            icon = icons_cfg.get("critical", icon)

        if charging:
            icon = icons_cfg.get("charging", icon) + icon

        fmt = battery_cfg.get("format", "{icon} {percentage}%")
        self.set_label(fmt.format(icon=icon, percentage=int(perc)))
