import re
import asyncio

from ignis import widgets, utils
from ignis.window_manager import WindowManager
from ignis.services.applications import (
    ApplicationsService,
    Application,
    ApplicationAction,
)
from ignis.menu_model import IgnisMenuModel, IgnisMenuItem, IgnisMenuSeparator

from gi.repository import Gio, Gtk  # type: ignore

from config import config, user_config

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


class CustomActionItem(widgets.Button):
    pass


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
                ]
            ),
        )
        self.__sync_menu()
        application.connect("notify::is-pinned", lambda x, y: self.__sync_menu())

    def launch(self) -> None:
        self._application.launch(terminal_format=TERMINAL_FORMAT)
        window_manager.close_window(f"{config.NAMESPACE}_launcher")

    def launch_action(self, action: ApplicationAction) -> None:
        action.launch()
        window_manager.close_window(f"{config.NAMESPACE}_launcher")

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
                ]
            ),
        )

    def launch(self) -> None:
        asyncio.create_task(utils.exec_sh_async(f"xdg-open {self._url}"))
        window_manager.close_window(f"{config.NAMESPACE}_launcher")


class Launcher(widgets.Window):
    def __init__(self):
        self.MAX_ITEMS = 78
        self._app_list = widgets.Grid(
            column_homogeneous=True,
            row_homogeneous=True,
            hexpand=True,
            vexpand=True,
            halign="center",
            valign="start",
        )
        self._added_items = []

        self._entry = widgets.Entry(
            hexpand=True,
            placeholder_text="Search",
            css_classes=["launcher-search"],
            on_change=self.__search,
            on_accept=self.__on_accept,
        )

        main_box = widgets.Box(
            vertical=True,
            valign="end",
            halign="center",
            css_classes=["launcher"],
            child=[
                self._app_list,
                widgets.Box(
                    css_classes=["launcher-search-box"],
                    child=[
                        widgets.Icon(
                            icon_name="system-search-symbolic",
                            pixel_size=24,
                            style="margin-right: 0.5rem;",
                        ),
                        self._entry,
                    ],
                ),
            ],
        )
        self._main_box = main_box

        super().__init__(
            namespace=f"{config.NAMESPACE}_launcher",
            visible=False,
            popup=True,
            kb_mode="on_demand",
            css_classes=["unset"],
            setup=lambda self: self.connect("notify::visible", self.__on_open),
            anchor=["top", "right", "bottom", "left"],
            child=widgets.Overlay(
                child=widgets.Button(
                    vexpand=True,
                    hexpand=True,
                    can_focus=False,
                    css_classes=["unset"],
                    on_click=lambda x: window_manager.close_window(
                        f"{config.NAMESPACE}_launcher"
                    ),
                    style="background-color: rgba(0, 0, 0, 0.3);",
                ),
                overlays=[main_box],
            ),
            style="background-color: rgba(0, 0, 0, 0.7);",
        )

        self.__show_all_apps()

    def __show_all_apps(self):
        apps = applications.apps
        self._populate_grid(apps[:self.MAX_ITEMS])

    def __on_open(self, *args) -> None:
        if not self.visible:
            return

        self._entry.text = ""
        self._entry.grab_focus()

    def __on_accept(self, *args) -> None:
        if self._added_items:
            self._added_items[0].launch()

    def _populate_grid(self, items):
        for item in self._added_items:
            self._app_list.remove(item)
        self._added_items.clear()

        if not items:
            return

        columns = 6
        for idx, item in enumerate(items):
            row = idx // columns
            col = idx % columns

            widget = LauncherAppItem(item) if isinstance(item, Application) else item
            self._app_list.attach(widget, col, row, 1, 1)
            self._added_items.append(widget)

    def __search(self, *args) -> None:
        query = self._entry.text.strip()

        if query == "":
            self.__show_all_apps()
            return

        filtered = applications.search(applications.apps, query)
        if not filtered:
            self._populate_grid([SearchWebButton(query)])
        else:
            self._populate_grid(filtered[:self.MAX_ITEMS])
