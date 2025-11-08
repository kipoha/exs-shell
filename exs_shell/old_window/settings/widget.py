import os
import getpass
import asyncio

from ignis import utils, widgets
from ignis.services.fetch import FetchService

from base.singleton import SingletonClass

from config import config
from config.user import options

from window.settings.active_page import active_page
from window.settings.pages import (
    AboutEntry,
    NotificationsEntry,
    TestEntry,
    BarEntry,
    AppearanceEntry,
    WifiEntry,
    BluetoothEntry,
    WeatherEntry,
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
        self._avatar = widgets.Picture(
            css_classes=["settings-sidebar-user-avatar-image"],
            image=options.user_config.avatar,
            width=80,
            height=80,
            content_fit="cover",
        )

        user_profile = widgets.Box(
            css_classes=["settings-sidebar-user"],
            spacing=10,
            child=[
                widgets.Button(
                    on_click=lambda x: asyncio.create_task(self.__change_avatar()),
                    css_classes=["settings-sidebar-user-avatar"],
                    child=self._avatar,
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
                            css_classes=["settings-sidebar-user-os"],
                        ),
                        widgets.Label(
                            label=utils.Poll(
                                60_000,
                                lambda _: f"{fetch.uptime[0]} Days, {fetch.uptime[1]} Hours, {fetch.uptime[2]} Minutes",
                            ).bind("output"),
                            halign="start",
                            css_classes=["settings-sidebar-user-uptime"],
                        ),
                    ],
                ),
            ],
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
            default_width=1600,
            default_height=900,
            resizable=False,
            hide_on_close=True,
            visible=False,
            child=widgets.Box(child=[navigation_sidebar, content]),
            namespace=f"{config.NAMESPACE}_settings",
            css_classes=["settings"],
        )

        self.connect("notify::visible", self.__on_open)

        options.user_config.connect_option("avatar", self._avatar_set_image)

    def _avatar_set_image(self, *_):
        self._avatar.set_image(options.user_config.avatar)

    async def __change_avatar(self):
        def change(self_, file):
            file_path = file.get_path()
            options.user_config.avatar = file_path
            self._avatar.set_image(file_path)

        dialog = widgets.FileDialog(
            initial_path=os.path.expanduser("~"),
            select_folder=False,
            filters=[
                widgets.FileFilter(
                    mime_types=["image/jpeg", "image/png"],
                    default=True,
                    name="Images JPEG/PNG",
                )
            ],
            on_file_set=change,
        )
        await dialog.open_dialog()

    def __on_open(self, *args) -> None:
        if self.visible is False:
            return

        if len(self._listbox.rows) != 0:  # type: ignore
            return

        rows = [
            AppearanceEntry(),
            BarEntry(),
            WeatherEntry(),
            WifiEntry(),
            BluetoothEntry(),
            NotificationsEntry(),
            AboutEntry(),
            TestEntry(),
        ]

        self._listbox.rows = rows  # type: ignore
        self._listbox.activate_row(rows[options.settings.last_page])

        self._listbox.connect("row-activated", self.__update_last_page)

    def __update_last_page(self, x, row) -> None:
        options.settings.last_page = self._listbox.rows.index(row)  # type: ignore
