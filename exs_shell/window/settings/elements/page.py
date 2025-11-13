from ignis import widgets
from ignis.base_widget import BaseWidget

from exs_shell.window.settings.elements.group import SettingsGroup


class SettingsPage(widgets.Scroll):
    def __init__(self, name: str, groups: list[SettingsGroup | BaseWidget] = []):
        super().__init__(
            hexpand=True,
            vexpand=True,
            child=widgets.Box(
                vertical=True,
                hexpand=True,
                vexpand=True,
                css_classes=["settings-page"],
                child=[
                    widgets.CenterBox(
                        center_widget=widgets.Box(
                            child=[
                                widgets.Corner(
                                    orientation="top-right",
                                    width_request=20,
                                    height_request=20,
                                    halign="start",
                                    valign="start",
                                    css_classes=["settings-page-header-left-corner"],
                                ),
                                widgets.Box(
                                    css_classes=["settings-page-header"],
                                    child=[
                                        widgets.Label(
                                            label=name,
                                            css_classes=["settings-page-name"],
                                            halign="center",
                                        )
                                    ]
                                ),
                                widgets.Corner(
                                    orientation="top-left",
                                    width_request=20,
                                    height_request=20,
                                    halign="start",
                                    valign="start",
                                    css_classes=["settings-page-header-right-corner"],
                                ),
                            ],
                        ),
                    ),
                    *groups,
                ],
            ),
        )
