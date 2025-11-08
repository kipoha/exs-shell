import re
import asyncio

from dataclasses import dataclass

from typing import Any

from ignis import widgets, utils
from ignis.window_manager import WindowManager
from ignis.services.applications import (
    ApplicationsService,
    Application,
    ApplicationAction,
)
from ignis.menu_model import IgnisMenuModel, IgnisMenuItem, IgnisMenuSeparator

from gi.repository import Gio, GLib  # type: ignore

from exs_shell.base.singleton import SingletonClass
from exs_shell.base.window.animated import AnimatedWindowPopup, PartiallyAnimatedWindow
from exs_shell.config import config
from exs_shell.config.user import options

window_manager = WindowManager.get_default()

applications = ApplicationsService.get_default()

TERMINAL_FORMAT = "kitty %command%"


def is_url(url: str) -> bool:
    regex = re.compile(
        r"^(?:http|ftp)s?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
        r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return re.match(regex, url) is not None


@dataclass
class Action:
    name: str
    command: str
    icon: str


class ActionItem(widgets.Button):
    def __init__(self, action: Action):
        self.action = action
        super().__init__(
            on_click=lambda x: self.launch(),
            css_classes=["launcher-app"],
            child=widgets.Box(
                child=[
                    widgets.Picture(image=self.action.icon, width=48, height=48),
                    widgets.Label(
                        label=self.action.name,
                        css_classes=["launcher-app-label"],
                    ),
                ],
                spacing=10,
            ),
        )

    def launch(self) -> None:
        asyncio.create_task(utils.exec_sh_async(self.action.command))
        window = window_manager.get_window(f"{config.NAMESPACE}_launcher")
        window.toggle()


class LauncherAppItem(widgets.Button):
    def __init__(self, application: Application) -> None:
        self._menu = widgets.PopoverMenu()

        self._application = application
        super().__init__(
            on_click=lambda x: self.launch(),
            on_right_click=lambda x: self._menu.popup(),
            css_classes=["launcher-app"],
            child=widgets.Box(
                child=[
                    widgets.Icon(image=application.icon, pixel_size=48),
                    widgets.Label(
                        label=application.name,
                        ellipsize="end",
                        max_width_chars=30,
                        css_classes=["launcher-app-label"],
                    ),
                    self._menu,
                ],
                spacing=10,
            ),
        )
        self.__sync_menu()
        application.connect("notify::is-pinned", lambda x, y: self.__sync_menu())

    def launch(self) -> None:
        self._application.launch(terminal_format=TERMINAL_FORMAT)
        window = window_manager.get_window(f"{config.NAMESPACE}_launcher")
        window.toggle()

    def launch_action(self, action: ApplicationAction) -> None:
        action.launch()
        window = window_manager.get_window(f"{config.NAMESPACE}_launcher")
        window.toggle()

    def __sync_menu(self) -> None:
        self._menu.model = IgnisMenuModel(
            IgnisMenuItem(label="Launch", on_activate=lambda x: self.launch()),
            IgnisMenuSeparator(),
            *(
                IgnisMenuItem(
                    label=i.name,
                    on_activate=lambda x, action=i: self.launch_action(action),
                )
                for i in self._application.actions
            ),
            IgnisMenuSeparator(),
            IgnisMenuItem(label="Pin", on_activate=lambda x: self._application.pin())
            if not self._application.is_pinned
            else IgnisMenuItem(
                label="Unpin", on_activate=lambda x: self._application.unpin()
            ),
        )


class SearchWebButton(widgets.Button):
    def __init__(self, query: str):
        self._query = query
        self._url = ""

        browser_desktop_file = utils.exec_sh(
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
            self._url = query
        else:
            label = "Search in Google"
            self._url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        super().__init__(
            on_click=lambda x: self.launch(),
            css_classes=["launcher-app"],
            child=widgets.Box(
                child=[
                    widgets.Icon(image=icon_name, pixel_size=48),
                    widgets.Label(
                        label=label,
                        css_classes=["launcher-app-label"],
                    ),
                ],
                spacing=10,
            ),
        )

    def launch(self) -> None:
        asyncio.create_task(utils.exec_sh_async(f"xdg-open {self._url}"))
        window = window_manager.get_window(f"{config.NAMESPACE}_launcher")
        window.toggle()


class Launcher(PartiallyAnimatedWindow, AnimatedWindowPopup, SingletonClass):
    def __init__(self):
        self.MAX_ITEMS = 5

        self.current_items = applications.apps[: self.MAX_ITEMS]

        self._entry = widgets.Entry(
            hexpand=True,
            placeholder_text="Search",
            css_classes=["launcher-search"],
            on_change=self.__search,
            on_accept=self.__on_accept,
        )

        self._list_box = widgets.Box(
            vertical=True,
            spacing=4,
            css_classes=["launcher-app-list"],
        )
        self._scroll = widgets.Scroll(
            vexpand=True,
            hexpand=True,
            child=self._list_box,
            css_classes=["launcher-scroll"],
        )

        self.left_corner = widgets.Corner(
            css_classes=["launcher-left-corner"],
            orientation="bottom-right",
            width_request=50,
            height_request=70,
            halign="end",
            valign="end",
        )
        self.right_corner = widgets.Corner(
            css_classes=["launcher-right-corner"],
            orientation="bottom-left",
            width_request=50,
            height_request=70,
            halign="end",
            valign="end",
        )

        self._box = widgets.Box(
            vertical=True,
            valign="end",
            halign="center",
            css_classes=["launcher", "hidden"],
            spacing=15,
            child=[
                self._scroll,
                widgets.Box(
                    css_classes=["launcher-search-box"],
                    child=[
                        widgets.Icon(
                            icon_name="system-search-symbolic",
                            pixel_size=20,
                            style="margin-right: 0.5rem;",
                        ),
                        self._entry,
                    ],
                ),
            ],
        )

        self._main_box = widgets.Box(
            css_classes=["launcher-main"],
            child=[self.left_corner, self._box, self.right_corner],
        )

        self._animated_parts = [self.left_corner, self.right_corner, self._box]

        self._background_button = widgets.Button(
            vexpand=True,
            hexpand=True,
            can_focus=False,
            css_classes=["launcher-backdrop"],
            on_click=lambda x: self.close(),
        )

        super().__init__(
            namespace=f"{config.NAMESPACE}_launcher",
            visible=False,
            kb_mode="exclusive",
            anchor=["bottom"],
            child=widgets.Box(
                css_classes=["launcher-overlay"],
                child=[self._background_button, self._main_box],
            ),
        )

        self._added_items = []
        self._populate_box(self.current_items)

        self.actions = [Action(**action) for action in options.user_config.actions]
        options.user_config.connect_option("actions", self.update_actions)

    def update_actions(self):
        self.actions = [Action(**action) for action in options.user_config.actions]

    def open(self):
        window_manager.get_window(f"{config.NAMESPACE}_clipboard").close()
        window_manager.get_window(f"{config.NAMESPACE}_notification").close()
        if not self._is_open:
            super().open()
            self.__on_open()

    def __on_open(self):
        if not self.visible:
            return
        self._entry.text = ""
        self._entry.grab_focus()

    def _populate_box(self, items: list[Any]):
        for item in self._added_items:
            self._list_box.remove(item)
        self._added_items.clear()

        for item in items:
            if isinstance(item, widgets.Widget):
                widget = item
            elif isinstance(item, Application):
                widget = LauncherAppItem(item)
            else:
                widget = item
            self._list_box.append(widget)
            self._added_items.append(widget)

        height = min(len(items) * 75 + 90, 500)
        self._animate_height(height)

    def _animate_height(self, target_height, duration=0.25):
        start_height = self._box.get_allocated_height()
        start_time = GLib.get_monotonic_time()

        def update():
            elapsed = (GLib.get_monotonic_time() - start_time) / 1_000_000
            t = min(elapsed / duration, 1.0)
            t_smooth = 1 - pow(1 - t, 3)
            new_height = round(start_height + (target_height - start_height) * t_smooth)
            self._box.set_size_request(-1, new_height)
            if t < 1.0:
                return True
            else:
                return False

        GLib.idle_add(update)

    def __on_accept(self, *_):
        if self._added_items:
            first_item = self._added_items[0]
            if hasattr(first_item, "launch"):
                first_item.launch()

    def __search(self, *args):
        query = self._entry.text.lower().strip()
        if not query:
            self.current_items = applications.apps[: self.MAX_ITEMS]
            self._populate_box(self.current_items)
            return

        prefix = options.user_config.command_prefix
        if query.startswith(prefix):
            filtered = [
                ActionItem(action)
                for action in self.actions
                if query.replace(prefix, "") in action.name.lower().strip()
            ]
            self.current_items = filtered
            self._populate_box(filtered)
            return

        filtered = applications.search(applications.apps, query)
        if filtered:
            self.current_items = filtered[: self.MAX_ITEMS]
            self._populate_box(filtered[: self.MAX_ITEMS])
        else:
            self.current_items = [SearchWebButton(query)]
            self._populate_box([SearchWebButton(query)])
