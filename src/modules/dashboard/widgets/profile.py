import os
import getpass
import asyncio

from ignis import widgets, utils
from ignis.services.fetch import FetchService

from config.user import options


fetch = FetchService.get_default()


class UserProfile(widgets.Box):
    def __init__(self):
        self._avatar = widgets.Picture(
            css_classes=["dashboard-widget-profile-avatar-image"],
            image=options.user_config.avatar,
            width=100,
            height=100,
            content_fit="cover",
        )
        self._avatar_box = widgets.Button(
            on_click=lambda x: asyncio.create_task(self.__change_avatar()),
            css_classes=["dashboard-widget-profile-avatar"],
            child=self._avatar,
        )
        self._profile_box = widgets.Box(
            vertical=True,
            valign="center",
            css_classes=["dashboard-widget-profile-user-info"],
            child=[
                widgets.Label(
                    label=os.getenv("USER") or getpass.getuser(),
                    halign="start",
                    css_classes=["dashboard-widget-profile-user-name"],
                ),
                widgets.Label(
                    label=fetch.os_name,
                    halign="start",
                    css_classes=["dashboard-widget-profile-user-os"],
                ),
                widgets.Label(
                    label=utils.Poll(
                        60_000,
                        lambda _: f"{fetch.uptime[0]} Days, {fetch.uptime[1]} Hours, {fetch.uptime[2]} Minutes",
                    ).bind("output"),
                    halign="start",
                    css_classes=["dashboard-widget-profile-user-uptime"],
                ),
            ],
        )

        super().__init__(
            spacing=10,
            css_classes=["dashboard-widget-profile"],
            vexpand=True,
            hexpand=True,
            child=[
                self._avatar_box,
                self._profile_box,
            ],
        )

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
