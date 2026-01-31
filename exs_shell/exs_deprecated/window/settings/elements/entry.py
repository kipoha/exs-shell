from ignis import widgets
from ..elements.page import SettingsPage


class SettingsEntry(widgets.ListBoxRow):
    def __init__(
        self,
        icon: str,
        label: str,
        page: SettingsPage,
        **kwargs,
    ):
        from ..active_page import active_page

        super().__init__(
            child=widgets.Box(
                child=[
                    widgets.Label(
                        label=icon,
                        css_classes=["settings-sidebar-entry-icon"],
                    ),
                    widgets.Box(hexpand=True, vexpand=True),
                    widgets.Label(
                        label=label,
                        css_classes=["settings-sidebar-entry-label"],
                    ),
                ],
            ),
            css_classes=["settings-sidebar-entry"],
            on_activate=lambda x: active_page.set_value(page),
            **kwargs,
        )
