import os
import getpass

from typing import Any

from ignis.widgets import Label, Separator, Picture, Box, Button, FileDialog, FileFilter
from ignis.services.fetch import FetchService

from exs_shell import register
from exs_shell.configs.user import user
from exs_shell.state import State
from exs_shell.utils.loop import run_async_task
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    DialogRow,
    SwitchRow,
)


class UserCategory(BaseCategory):
    def __init__(self):
        self.fetch: FetchService = State.services.fetch
        self.user_avatar = Picture(
            image=user.avatar,
            content_fit="cover",
            width=70,
            height=70,
            css_classes=["settings-user-avatar"],
        )
        self.avatar_button = Button(
            css_classes=["settings-user-avatar-button"],
            child=self.user_avatar,
            on_click=lambda _: run_async_task(self.__change_avatar()),
        )
        self.uptime = Label(
            label=self.format_uptime(self.fetch.uptime),
            css_classes=["settings-user-uptime"],
            halign="start",
        )
        self.username = Label(
            label=os.getenv("USER") or getpass.getuser(),
            css_classes=["settings-user-name"],
            halign="start",
        )
        self.user_data = Box(
            vertical=True,
            child=[self.username, self.uptime],
            css_classes=["settings-user-data"],
            valign="center",
        )
        self.userspace = Box(
            child=[self.avatar_button, self.user_data],
            css_classes=["settings-user-container"],
            spacing=5,
        )

        super().__init__(
            child=[
                CategoryLabel(title="User", icon=Icons.ui.USER),
                self.userspace,
            ]
        )

    def format_uptime(self, uptime: tuple[int, int, int]) -> str:
        return f"{uptime[0]} Days, {uptime[1]} Hours, {uptime[2]} Minutes"

    @register.events.option(user, "avatar")
    def __on_avatar_changed(self, *_: Any) -> None:
        self.user_avatar.set_image(user.avatar)

    @register.events.poll(1_000)
    def __on_uptime_changed(self, *_: Any) -> None:
        self.uptime.set_label(self.format_uptime(self.fetch.uptime))

    async def __change_avatar(self):
        def change(self_, file):
            file_path = file.get_path()
            user.avatar = file_path
            self.user_avatar.set_image(file_path)

        dialog = FileDialog(
            initial_path=os.path.expanduser("~"),
            select_folder=False,
            filters=[
                FileFilter(
                    mime_types=["image/jpeg", "image/png", "image/webp", "image/gif"],
                    default=True,
                    name="Images JPEG/PNG",
                )
            ],
            on_file_set=change,
        )
        await dialog.open_dialog()


class MainTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                UserCategory(),
            ]
        )
