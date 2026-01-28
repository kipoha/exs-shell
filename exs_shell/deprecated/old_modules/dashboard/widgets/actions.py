import subprocess

from ignis import widgets
from ignis.window_manager import WindowManager

from exs_shell.config import config


class Actions(widgets.Box):
    def __init__(self):
        self.settings_button = widgets.Button(
            child=widgets.Label(label=""),
            on_click=self.run_settings,
            css_classes=["dashboard-widget-actions-settings"],
        )
        self.browser_button = widgets.Button(
            child=widgets.Label(label=""),
            on_click=self.run_browser,
            css_classes=["dashboard-widget-actions-browser"],
        )
        self.terminal_button = widgets.Button(
            child=widgets.Label(label=""),
            on_click=self.run_terminal,
            css_classes=["dashboard-widget-actions-terminal"],
        )
        super().__init__(
            spacing=2,
            vertical=True,
            valign="center",
            css_classes=["dashboard-widget-actions"],
            child=[
                self.settings_button,
                self.browser_button,
                self.terminal_button,
            ],
        )

    def run_settings(self, *_):
        window_manager = WindowManager.get_default()
        window_manager.toggle_window(f"{config.NAMESPACE}_settings")

    def run_browser(self, *_):
        subprocess.Popen(["firefox"])

    def run_terminal(self, *_):
        subprocess.Popen(["kitty"])
