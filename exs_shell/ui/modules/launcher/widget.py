from typing import Any

from ignis.menu_model import IgnisMenuModel, IgnisMenuItem, IgnisMenuSeparator
from ignis.utils import exec_sh, exec_sh_async
from ignis.widgets import (
    Button,
    Entry,
    Scroll,
    Widget,
    Corner,
    Box,
    Label,
    Icon,
    Picture,
    PopoverMenu,
)
from ignis.services.applications import (
    ApplicationsService,
    Application,
    ApplicationAction,
)

from gi.repository import Gio, GLib  # type: ignore

from exs_shell import register
from exs_shell.configs.user import user
from exs_shell.interfaces.enums.gtk.windows import KeyboardMode
from exs_shell.interfaces.schemas.widget.launcher import Action
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.state import State
from exs_shell.utils import window
from exs_shell.utils.loop import run_async_task
from exs_shell.utils.urls import is_url
from exs_shell.ui.factory import window as window_factory
from exs_shell.ui.widgets.base import RevealerBaseWidget


class ActionItem(Button):
    def __init__(self, action: Action):
        self.action = action
        super().__init__(
            on_click=lambda x: self.launch(),
            css_classes=["launcher-app"],
            child=Box(
                child=[
                    Picture(image=self.action.icon, width=48, height=48),
                    Label(
                        label=self.action.name,
                        css_classes=["launcher-app-label"],
                    ),
                ],
                spacing=10,
            ),
        )

    def launch(self) -> None:
        run_async_task(exec_sh_async(self.action.command))
        _window = window.get("launcher")
        _window.set_visible(False)


class LauncherAppItem(Button):
    def __init__(self, application: Application) -> None:
        self._menu = PopoverMenu()

        self._application = application
        super().__init__(
            on_click=lambda x: self.launch(),
            on_right_click=lambda x: self._menu.popup(),
            css_classes=["launcher-app"],
            child=Box(
                child=[
                    Icon(image=application.icon, pixel_size=48),
                    Label(
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
        self._application.launch(terminal_format=user.terminal_format)
        _window = window.get("launcher")
        _window.set_visible(False)

    def launch_action(self, action: ApplicationAction) -> None:
        action.launch()
        _window = window.get("launcher")
        _window.set_visible(False)

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


class SearchWebButton(Button):
    def __init__(self, query: str):
        self._query = query
        self._url = ""

        browser_desktop_file = exec_sh(
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
            child=Box(
                child=[
                    Icon(image=icon_name, pixel_size=48),
                    Label(
                        label=label,
                        css_classes=["launcher-app-label"],
                    ),
                ],
                spacing=10,
            ),
        )

    def launch(self) -> None:
        run_async_task(exec_sh_async(f"xdg-open {self._url}"))
        _window = window.get("launcher")
        _window.set_visible(False)


@register.window
@register.event
class Launcher(RevealerBaseWidget):
    MAX_ITEMS = 5

    def __init__(
        self,
        transition_duration: int = 300,
        reveal_child: bool = True,
    ) -> None:
        self.applications: ApplicationsService = State.services.applications
        self.current_items = self.applications.apps[: self.MAX_ITEMS]
        self._entry = Entry(
            hexpand=True,
            placeholder_text="Search",
            css_classes=["exs-launcher-search"],
            on_change=self.__search,
            on_accept=self.__on_accept,
        )

        self._list_box = Box(
            vertical=True,
            spacing=4,
            css_classes=["exs-launcher-app-list"],
        )
        self._scroll = Scroll(
            vexpand=True,
            hexpand=True,
            child=self._list_box,
            css_classes=["exs-launcher-scroll"],
        )

        self.left_corner = Corner(
            css_classes=["exs-launcher-left-corner"],
            orientation="bottom-right",
            width_request=50,
            height_request=70,
            halign="end",
            valign="end",
        )
        self.right_corner = Corner(
            css_classes=["exs-launcher-right-corner"],
            orientation="bottom-left",
            width_request=50,
            height_request=70,
            halign="end",
            valign="end",
        )

        self._search_box = Box(
            vertical=True,
            valign="end",
            halign="center",
            css_classes=["exs-launcher-box"],
            spacing=15,
            child=[
                self._scroll,
                Box(
                    css_classes=["exs-launcher-search-box"],
                    child=[
                        Icon(
                            icon_name="system-search-symbolic",
                            pixel_size=20,
                            style="margin-right: 0.5rem;",
                        ),
                        self._entry,
                    ],
                ),
            ],
        )

        self._box = Box(
            child=[
                self.left_corner,
                self._search_box,
                self.right_corner,
            ],
            css_classes=["exs-launcher"],
        )

        window_param = window_factory.create(
            namespace="launcher",
            visible=False,
            kb_mode=KeyboardMode.ON_DEMAND,
            anchor=["bottom"],
            popup=True,
        )
        super().__init__(
            self._box,
            window_param,
            RevealerTransition.SLIDE_UP,
            transition_duration,
            reveal_child,
        )

        self._added_items = []
        self._populate_box(self.current_items)

        self.update_actions()

    @register.events.option(user, "actions")
    def update_actions(self):
        self.actions = [Action(**action) for action in user.actions]

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
            if isinstance(item, Widget):
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

    def __search(self, *_):
        query = self._entry.text.lower().strip()
        if not query:
            self.current_items = self.applications.apps[: self.MAX_ITEMS]
            self._populate_box(self.current_items)
            return

        prefix = user.command_prefix
        if query.startswith(prefix):
            filtered = [
                ActionItem(action)
                for action in self.actions
                if query.replace(prefix, "") in action.name.lower().strip()
            ]
            self.current_items = filtered
            self._populate_box(filtered)
            return

        filtered = self.applications.search(self.applications.apps, query)
        if filtered:
            self.current_items = filtered[: self.MAX_ITEMS]
            self._populate_box(filtered[: self.MAX_ITEMS])
        else:
            bb = SearchWebButton(query)
            self.current_items = [bb]
            self._populate_box([bb])
