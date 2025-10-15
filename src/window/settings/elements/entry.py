from ignis import widgets
from window.settings.elements.page import SettingsPage


class SettingsEntry(widgets.ListBoxRow):
    def __init__(
        self,
        icon: str,
        label: str,
        page: SettingsPage,
        **kwargs,
    ):
        from window.settings.active_page import active_page

        super().__init__(
            child=widgets.Box(
                child=[
                    widgets.Icon(image=icon, pixel_size=20),
                    widgets.Label(label=label, style="margin-left: 0.75rem;"),
                ],
            ),
            css_classes=["settings-sidebar-entry"],
            on_activate=lambda x: active_page.set_value(page),
            **kwargs,
        )
