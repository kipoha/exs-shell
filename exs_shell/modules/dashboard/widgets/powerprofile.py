import subprocess

from ignis import widgets

from exs_shell.utils import send_notification


class PowerProfile(widgets.Box):
    def __init__(self):
        self.performance_button = widgets.Button(
            child=widgets.Label(label="󰓅"),
            on_click=self.set_performance,
            css_classes=["dashboard-widget-power-profile-performance"],
        )
        self.balanced_button = widgets.Button(
            child=widgets.Label(label=""),
            on_click=self.set_balanced,
            css_classes=["dashboard-widget-power-profile-balanced"],
        )
        self.power_save_button = widgets.Button(
            child=widgets.Label(label="󰌪"),
            on_click=self.set_power_saver,
            css_classes=["dashboard-widget-power-profile-power-save"],
        )
        super().__init__(
            spacing=2,
            vertical=True,
            valign="center",
            css_classes=["dashboard-widget-power-profile"],
            child=[
                self.performance_button,
                self.balanced_button,
                self.power_save_button,
            ],
        )

        self.highlight_active_profile()

    def set_profile(self, profile: str, label: str):
        subprocess.run(["powerprofilesctl", "set", profile])
        send_notification("Power Profile", f"Set to {label}")
        self.highlight_active_profile()

    def set_performance(self, *_):
        self.set_profile("performance", "󰓅 Performance")

    def set_balanced(self, *_):
        self.set_profile("balanced", " Balanced")

    def set_power_saver(self, *_):
        self.set_profile("power-saver", "󰌪 Power Save")

    def highlight_active_profile(self):
        for button in [
            self.performance_button,
            self.balanced_button,
            self.power_save_button,
        ]:
            button.remove_css_class("active")

        result = subprocess.run(
            ["powerprofilesctl", "get"], capture_output=True, text=True
        )
        current = result.stdout.strip()

        match current:
            case "performance":
                self.performance_button.add_css_class("active")
            case "balanced":
                self.balanced_button.add_css_class("active")
            case "power-saver":
                self.power_save_button.add_css_class("active")
            case _:
                pass
