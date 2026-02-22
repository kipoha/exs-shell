from ignis import widgets
from ignis.services.upower import UPowerService

from exs_shell_deprecated.config.user import options



class Battery(widgets.Label):
    def __init__(self):
        self.battery_cfg = options.user_config.battery
        super().__init__(
            label=self.battery_cfg.get("format", "{icon} {percentage}%").format(
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
        options.user_config.connect_option("battery", self.update_battery)

    def _update_label(self):
        perc = self.battery.get_property("percent") or 0
        charging = bool(
            self.battery.get_property("charging")
            or self.battery.get_property("charged")
        )

        icons_cfg = self.battery_cfg.get("icons", {})
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

        if perc <= self.battery_cfg.get("critical_level", 10):
            icon = icons_cfg.get("critical", icon)

        if charging:
            icon = icons_cfg.get("charging", icon) + icon

        fmt = self.battery_cfg.get("format", "{icon} {percentage}%")
        self.set_label(fmt.format(icon=icon, percentage=int(perc)))

    def update_battery(self, *args):
        self.battery_cfg = options.user_config.battery
        self._update_label()
