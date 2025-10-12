from ignis import widgets
from base.singleton import SingletonClass
from config import config
from config.user import options
from .active_page import active_page
from .pages import (
    AboutEntry,
)


class Settings(widgets.RegularWindow, SingletonClass):

    def __init__(self) -> None:
        content = widgets.Box(
            hexpand=True,
            vexpand=True,
            child=active_page.bind("value", transform=lambda value: [value]),
        )
        self._listbox = widgets.ListBox()

        navigation_sidebar = widgets.Box(
            vertical=True,
            css_classes=["settings-sidebar"],
            child=[
                widgets.Label(
                    label="Settings",
                    halign="start",
                    css_classes=["settings-sidebar-label"],
                ),
                self._listbox,
            ],
        )

        super().__init__(
            default_width=900,
            default_height=600,
            resizable=False,
            hide_on_close=True,
            visible=False,
            child=widgets.Box(child=[navigation_sidebar, content]),
            namespace=f"{config.NAMESPACE}_settings",
            css_classes=["settings"],
        )

        self.connect("notify::visible", self.__on_open)

    def __on_open(self, *args) -> None:
        if self.visible is False:
            return

        if len(self._listbox.rows) != 0:
            return

        rows = [
            AboutEntry(),
        ]

        self._listbox.rows = rows
        self._listbox.activate_row(rows[options.settings.last_page])

        self._listbox.connect("row-activated", self.__update_last_page)

    def __update_last_page(self, x, row) -> None:
        options.settings.last_page = self._listbox.rows.index(row)
