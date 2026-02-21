import subprocess
from typing import Any

from gi.repository import Gio, GdkPixbuf  # type: ignore

from ignis.menu_model import IgnisMenuItem, IgnisMenuModel, IgnisMenuSeparator
from ignis.services.applications import Application, ApplicationAction
from ignis.utils import exec_sh, exec_sh_async
from ignis.widgets import Box, Button, Icon, Label, Picture, PopoverMenu

from exs_shell import register
from exs_shell.configs.user import user
from exs_shell.interfaces.schemas.utils.clipboard import ClipboardItem
from exs_shell.interfaces.schemas.widget.launcher import (
    Action,
    PowerMenuAction,
    WebAction,
)
from exs_shell.utils import window
from exs_shell.utils.loop import run_async_task
from exs_shell.utils.urls import is_url


class BaseLauncherItem(Button):
    def __init__(
        self,
        item: Application | Action | WebAction | PowerMenuAction | None = None,
        icon: Icon | Picture | None = None,
    ):
        if icon:
            icon.add_css_class("exs-launcher-app-icon")
        children = [icon] if icon else []

        if item:
            children.append(
                Label(label=item.name, css_classes=["exs-launcher-app-label"])
            )
        content_box = Box(child=children, spacing=10)
        super().__init__(
            child=content_box,
            on_click=self.launch,
            focusable=False,
            can_focus=False,
            css_classes=["exs-launcher-app"],
        )

    def close_launcher(self) -> None:
        _window = window.get("launcher")
        _window.set_visible(False)

    def launch(self, *_: Any) -> None:
        self.close_launcher()


class ActionItem(BaseLauncherItem):
    def __init__(self, action: Action | PowerMenuAction, scale: float = 1.0):
        self.action = action
        super().__init__(
            action,
            Icon(image=self.action.icon, pixel_size=48 * scale),  # type: ignore
        )

    def launch(self, *_: Any) -> None:
        cmd = self.action.command
        if "{terminal_format}" in cmd:
            inner = cmd.replace("{terminal_format}", "").strip()
            cmd = user.terminal_format.replace("%command%", inner)
        run_async_task(exec_sh_async(cmd))
        super().launch(*_)


@register.event
class LauncherAppItem(BaseLauncherItem):
    def __init__(self, application: Application, scale: float = 1.0) -> None:
        self._menu = PopoverMenu()

        self._application = application
        super().__init__(
            application,
            Icon(image=application.icon, pixel_size=48 * scale),  # type: ignore
        )
        self.__sync_menu()

    def launch(self, *_: Any) -> None:
        self._application.launch(terminal_format=user.terminal_format)
        super().launch(*_)

    def launch_action(self, _: Any, action: ApplicationAction) -> None:
        action.launch()
        self.close_launcher()

    @register.events.applications("notify::is-pinned")
    def __sync_menu(self, *_: Any) -> None:
        self._menu.model = IgnisMenuModel(
            IgnisMenuItem(label="Launch", on_activate=self.launch),
            IgnisMenuSeparator(),
            *(
                IgnisMenuItem(
                    label=i.name,
                    on_activate=self.launch_action,
                )
                for i in self._application.actions
            ),
            IgnisMenuSeparator(),
            IgnisMenuItem(label="Pin", on_activate=lambda _: self._application.pin())
            if not self._application.is_pinned
            else IgnisMenuItem(
                label="Unpin", on_activate=lambda _: self._application.unpin()
            ),
        )


class SearchWebButton(BaseLauncherItem):
    def __init__(self, query: str, scale: float = 1.0):
        self._query = query
        browser_desktop_file: str = exec_sh(
            "xdg-settings get default-web-browser"
        ).stdout.replace("\n", "")

        app_info = Gio.DesktopAppInfo.new(desktop_id=browser_desktop_file)

        icon_name = "applications-internet-symbolic"
        if app_info:
            icon_string = app_info.get_string("Icon")
            if icon_string:
                icon_name = icon_string

        if not query.startswith(("http://", "https://")) and "." in query:
            query = "https://" + query

        if is_url(query):
            label = f"Visit {query}"
            url = query
        else:
            label = "Search in Google"
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        self.action = WebAction(
            name=label,
            url=url,
            icon=icon_name,
        )

        super().__init__(
            self.action,
            Icon(image=icon_name, pixel_size=48 * scale),  # type: ignore
        )

    def launch(self, *_: Any) -> None:
        run_async_task(exec_sh_async(f"xdg-open {self.action.url}"))
        super().launch(*_)


class ClipboardItemButton(BaseLauncherItem):
    def __init__(self, clipboard: ClipboardItem, scale: float = 1.0):
        self.clipboard = clipboard
        if clipboard.is_binary:
            try:
                image_bytes = subprocess.run(
                    ["cliphist", "decode", clipboard.id], capture_output=True
                ).stdout
                loader = GdkPixbuf.PixbufLoader.new()
                loader.write(image_bytes)
                loader.close()
                pixbuf = loader.get_pixbuf()
                target_height = 80 * scale
                scale = target_height / pixbuf.get_height()
                pixbuf = pixbuf.scale_simple(
                    int(pixbuf.get_width() * scale),
                    target_height,
                    GdkPixbuf.InterpType.BILINEAR,
                )
                image = Picture(
                    image=pixbuf,
                    width=pixbuf.get_width(),
                    height=target_height,  # type: ignore
                    content_fit="cover",
                    css_classes=["exs-clipboard-image"],
                )
                box = Box(
                    spacing=6,
                    child=[image],
                    hexpand=True,
                    css_classes=["exs-clipboard-item"],
                )
            except Exception as e:
                print(e)
                box = Box(
                    spacing=6,
                    child=[Label(label="[image]")],
                    hexpand=True,
                    css_classes=["exs-clipboard-item"],
                )
        else:
            text = clipboard.raw.split("\t")[-1]
            if len(text) > 60:
                text = text[:57] + "..."
            label = Label(label=text)
            box = Box(
                spacing=6,
                child=[label],
                hexpand=True,
                css_classes=["exs-clipboard-item"],
            )

        super().__init__()
        self.set_child(box)

    def launch(self, *_: Any) -> None:
        super().launch(*_)
        run_async_task(exec_sh_async(f"cliphist decode {self.clipboard.id} | wl-copy"))
