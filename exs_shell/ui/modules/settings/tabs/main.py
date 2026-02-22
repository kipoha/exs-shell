import os
import getpass

from typing import Any

from ignis.widgets import (
    Label,
    Separator,
    Picture,
    Box,
    Button,
    FileDialog,
    FileFilter,
    Overlay,
)
from ignis.services.fetch import FetchService

from exs_shell import register
from exs_shell.configs.user import bar, user, notifications, appearance
from exs_shell.interfaces.enums.configs.position import TopBottom
from exs_shell.state import State
from exs_shell.utils.loop import run_async_task
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    SelectRow,
    SwitchRow,
    FileDialogRow,
)


class AppearanceCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel("Wallpaper", Icons.ui.IMAGE),
            ],
        )

        self.wallpaper_picture = Picture(
            height=300,
            width=560,
            vexpand=False,
            hexpand=False,
            content_fit="cover",
            css_classes=["settings-wallpaper-preview"],
            image=appearance.bind("wallpaper_path"),
        )

        self.wallpaper_filename_label = Label(
            label=os.path.basename(appearance.wallpaper_path or "")
            or "Click to set wallpaper",
            halign="start",
            valign="end",
            margin_start=10,
            margin_bottom=10,
            css_classes=["settings-wallpaper-filename-label"],
        )

        def on_file_set_handler(_, file):
            path = file.get_path()
            self._set_and_update_wallpaper(path)

        file_chooser_button = FileDialogRow(
            on_file_set_handler,
            button_name=Icons.ui.IMAGE_OFF,
            css_classes=["settings-wallpaper-button-overlay"],
            initial_path=appearance.wallpaper_path,
            filters=[
                FileFilter(
                    mime_types=[
                        "image/jpeg",
                        "image/png",
                        "image/webp",
                        "image/gif",
                    ],
                    default=True,
                    name="Images (PNG, JPG, WebP, GIF)",
                )
            ],
        )
        file_chooser_button.remove_css_class("settings-row-dialog-button")

        wallpaper_icon = Box(
            valign="fill",
            halign="fill",
            css_classes=["settings-wallpaper-icon"],
            child=[
                # Icon(
                #     label=Icons.ui.IMAGE,
                #     size="xxl",
                #     halign="center",
                #     valign="center",
                #     css_classes=["settings-wallpaper-icon-label"],
                # )
            ],
            can_target=False,
        )

        wallpaper_overlay = Overlay(
            css_classes=["settings-wallpaper-overlay"],
            child=self.wallpaper_picture,
        )

        wallpaper_overlay.add_overlay(self.wallpaper_filename_label)
        wallpaper_overlay.add_overlay(wallpaper_icon)
        wallpaper_overlay.add_overlay(file_chooser_button)

        self.append(wallpaper_overlay)

    def _set_and_update_wallpaper(self, path: str | None):
        if path:
            appearance.wallpaper_path = path
            self.wallpaper_picture.set_image(path)
            self.wallpaper_filename_label.label = os.path.basename(path)


class UserCategory(BaseCategory):
    def __init__(self):
        self.fetch: FetchService = State.services.fetch
        self.user_avatar = Picture(
            image=user.avatar,
            content_fit="cover",
            width=50,
            height=50,
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


class NotificationsCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel(title="Notifications", icon=Icons.ui.NOTIFICATIONS),
                SettingsRow(
                    Icons.ui.DND,
                    title="Do not disturb",
                    description="Show notifications",
                    child=[
                        SwitchRow(
                            active=notifications.bind("dnd"),
                            on_change=lambda _: notifications.set_dnd(_),
                        )
                    ],
                ),
            ]
        )


class BarCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel("Bar", Icons.ui.INTERFACE),
                SettingsRow(
                    Icons.ui.SHOW,
                    title="Show",
                    description="Show bar",
                    child=[
                        SwitchRow(
                            active=bar.bind("show"),
                            on_change=lambda active: bar.set_show(active),
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    Icons.align.TOP,
                    title="Position",
                    description="Bar position(top, bottom)",
                    child=[
                        SelectRow(
                            TopBottom.aligns,
                            lambda x: bar.set_position(x),
                            active=bar.position,
                            css_classes=["exs-bar-select-arrow"],
                        )
                    ],
                ),
            ]
        )


class MainTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                AppearanceCategory(),
                UserCategory(),
                NotificationsCategory(),
                BarCategory(),
            ]
        )
