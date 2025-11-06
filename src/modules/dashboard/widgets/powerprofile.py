import subprocess

from ignis import widgets

from utils import send_notification


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
            on_click=self.set_power_save,
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

    def set_performance(self, *_):
        subprocess.Popen(["powerprofilesctl", "set", "performance"])
        send_notification("Power Profile", "Set to 󰓅 Performance")
        self.highlight_active_profile()

    def set_balanced(self, *_):
        subprocess.Popen(["powerprofilesctl", "set", "balanced"])
        send_notification("Power Profile", "Set to  Balanced")
        self.highlight_active_profile()

    def set_power_save(self, *_):
        subprocess.Popen(["powerprofilesctl", "set", "power-saver"])
        send_notification("Power Profile", "Set to 󰌪 Power Save")
        self.highlight_active_profile()

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
