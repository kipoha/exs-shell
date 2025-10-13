import os
import getpass
import asyncio
from ignis import widgets
from ignis.services.fetch import FetchService
from base.singleton import SingletonClass
from config import config
from config.user import options
from .active_page import active_page
from .pages import (
    AboutEntry,
)


fetch = FetchService.get_default()


class Settings(widgets.RegularWindow, SingletonClass):

    def __init__(self) -> None:
        content = widgets.Box(
            hexpand=True,
            vexpand=True,
            child=active_page.bind("value", transform=lambda value: [value]),
        )
        self._listbox = widgets.ListBox()

        user_profile = widgets.Box(
            css_classes=["settings-sidebar-user"],
            child=[
                widgets.Button(
                    on_click=lambda x: asyncio.create_task(widgets.FileDialog().open_dialog()),
                    css_classes=["settings-sidebar-user-avatar"],
                    child=widgets.Picture(
                        image=options.user_config.avatar,
                        width=80,
                        height=80,
                    ),
                ),
                widgets.Box(
                    vertical=True,
                    css_classes=["settings-sidebar-user-info"],
                    child=[
                        widgets.Label(
                            label=os.getenv("USER") or getpass.getuser(),
                            halign="start",
                            css_classes=["settings-sidebar-user-name"],
                        ),
                        widgets.Label(
                            label=fetch.os_name,
                            halign="start",
                            css_classes=["settings-sidebar-user-email"],
                        ),
                    ],
                )
            ]
        )

        navigation_sidebar = widgets.Box(
            vertical=True,
            css_classes=["settings-sidebar"],
            child=[
                user_profile,
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
