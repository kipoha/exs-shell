import os
import getpass

from typing import Any

from ignis.widgets import Box, Button, CenterBox, Label, Picture
from ignis.services.fetch import FetchService

from exs_shell import register
from exs_shell.ui.widgets.custom.icon import Icon
from exs_shell.utils import window as win_utils
from exs_shell.utils.commands import run_command
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.state import State
from exs_shell.configs.user import user


@register.event
class UserWidget(CenterBox):
    def __init__(self, scale: float = 1.0, **kwargs: Any):
        self.scale = scale
        self.fetch: FetchService = State.services.fetch
        self.user_avatar = Picture(
            image=user.avatar,
            content_fit="cover",
            width=50 * self.scale,  # type: ignore
            height=50 * self.scale,  # type: ignore
            css_classes=["control-center-user-avatar"],
        )
        self.uptime = Label(
            label=self.format_uptime(self.fetch.uptime),
            css_classes=["control-center-user-uptime"],
            halign="start",
        )
        self.username = Label(
            label=os.getenv("USER") or getpass.getuser(),
            css_classes=["control-center-user-name"],
            halign="start",
        )
        self.user_data = Box(
            vertical=True,
            child=[self.username, self.uptime],
            css_classes=["control-center-user-data"],
            valign="center",
        )
        self.userspace = Box(
            child=[self.user_avatar, self.user_data],
            css_classes=["control-center-user-container"],
            spacing=5 * self.scale,
        )
        self.settings = Button(
            # child=Label(label=Icons.ui.SYSTEM),
            child=Icon(label=Icons.ui.SYSTEM, size="l"),
            css_classes=["control-center-user-buttons-settings"],
            on_click=lambda _: self.toggle_window("settings"),
            can_focus=False,
            focusable=False,
        )
        self.power_button = Button(
            # child=Label(label=Icons.ui.POWER),
            child=Icon(label=Icons.ui.POWER, size="l"),
            css_classes=["control-center-user-buttons-power"],
            on_click=lambda _: run_command("launcher", "powermenu"),
            can_focus=False,
            focusable=False,
        )
        self.buttons = Box(
            css_classes=["control-center-user-buttons"],
            spacing=4 * self.scale,
            child=[self.settings, self.power_button],
        )
        super().__init__(
            start_widget=self.userspace,
            end_widget=self.buttons,
            css_classes=["control-center-user"],
            hexpand=True,
            **kwargs,
        )

    def format_uptime(self, uptime: tuple[int, int, int]) -> str:
        return f"{uptime[0]} Days, {uptime[1]} Hours, {uptime[2]} Minutes"

    @register.events.option(user, "avatar")
    def __on_avatar_changed(self, *_: Any) -> None:
        self.user_avatar.set_image(user.avatar)

    @register.events.poll(1_000)
    def __on_uptime_changed(self, *_: Any) -> None:
        self.uptime.set_label(self.format_uptime(self.fetch.uptime))

    def toggle_window(self, window: str) -> None:
        win = win_utils.get("settings")
        win.set_visible(not win.visible)
