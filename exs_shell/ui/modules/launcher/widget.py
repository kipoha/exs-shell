from typing import Any

from ignis.widgets import Entry, Scroll, Corner, Box, Icon
from ignis.services.applications import ApplicationsService, Application

from gi.repository import GLib, Gdk, GLib  # type: ignore

from exs_shell import register
from exs_shell.configs.user import user
from exs_shell.interfaces.enums.gtk.windows import KeyboardMode
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.modules.launcher import LauncherMode
from exs_shell.state import State
from exs_shell.ui.factory import window as window_factory
from exs_shell.ui.modules.launcher.items import (
    ActionItem,
    ClipboardItemButton,
    LauncherAppItem,
    SearchWebButton,
)
from exs_shell.ui.widgets.base import MonitorRevealerBaseWidget
from exs_shell.utils.clipboard import get_clipboard_history


@register.window
@register.event
class Launcher(MonitorRevealerBaseWidget):
    MAX_ITEMS = 5

    def __init__(
        self,
        transition_duration: int = 300,
        reveal_child: bool = True,
    ) -> None:
        self.applications: ApplicationsService = State.services.applications
        self.current_items: list = self.applications.apps[: self.MAX_ITEMS]
        self.active_index: int = 0
        self.mode = LauncherMode.APPLICATIONS
        self.widget_build()

        window_param = window_factory.create(
            namespace="launcher",
            visible=False,
            kb_mode=KeyboardMode.EXCLUSIVE,
            anchor=["bottom"],
        )
        super().__init__(
            self._box,
            window_param,
            RevealerTransition.SLIDE_DOWN,
            transition_duration,
            reveal_child,
        )

        self._added_items = []
        self._refresh_items()
        self.update_actions()

    @register.events.option(user, "actions")
    def update_actions(self):
        self.actions = user.actions

    def widget_build(self) -> None:
        self._entry = Entry(
            hexpand=True,
            placeholder_text="Search",
            css_classes=["exs-launcher-search"],
            on_change=self.__search,
            can_focus=False,
            focusable=False,
        )
        self._list_box = Box(
            vertical=True,
            spacing=4,
            css_classes=["exs-launcher-app-list"],
        )
        self._scroll_app = Scroll(
            vexpand=True,
            hexpand=True,
            child=self._list_box,
            css_classes=["exs-launcher-scroll-app"],
            hscrollbar_policy="never",
        )
        self._search_box = Box(
            css_classes=["exs-launcher-search-box"],
            child=[
                Icon(
                    icon_name="system-search-symbolic",
                    pixel_size=20,
                    style="margin-right: 0.5rem;",
                ),
                self._entry,
            ],
        )
        self._inner = Box(
            vertical=True,
            valign="end",
            halign="center",
            css_classes=["exs-launcher"],
            spacing=15,
            child=[
                self._scroll_app,
                self._search_box,
            ],
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
        self._box = Box(
            child=[
                self.left_corner,
                self._inner,
                self.right_corner,
            ],
        )

    def __on_open(self):
        if not self.visible:
            return

    def _refresh_items(self):
        match self.mode:
            case LauncherMode.APPLICATIONS:
                items = self.applications.apps[: self.MAX_ITEMS]

            case LauncherMode.ACTIONS:
                items = [ActionItem(action, self.scale) for action in self.actions]

            case LauncherMode.CLIPBOARD:
                items = [
                    ClipboardItemButton(c, self.scale) for c in get_clipboard_history()
                ]
            case _:
                raise ValueError

        self.current_items = items
        self._populate_box(
            items, reset_index=True if self.active_index >= len(items) else False
        )

    @register.events.key_kontroller("key-pressed")
    def __on_key_released(self, controller, keyval, keycode, state):
        match keyval:
            case 65307:  # 65307 = ESC
                if self.mode != LauncherMode.APPLICATIONS:
                    self.mode = LauncherMode.APPLICATIONS
                    self._refresh_items()
                    self._entry.text = ""
                else:
                    self.set_visible(False)
            case 65362:  # 65362 = UP
                self._move_active(-1)
            case 65364:  # 65364 = DOWN
                self._move_active(1)
            case 65288:  # 65288 = BACKSPACE
                self._entry.text = self._entry.text[:-1]
            case 65293:  # 65293 = ENTER
                self.__on_accept()
            case _:
                char = Gdk.keyval_to_unicode(keyval)
                if char != 0:
                    self._entry.text += chr(char)

    def _populate_box(self, items: list[Any], reset_index: bool = True):
        for item in self._added_items:
            self._list_box.remove(item)
        self._added_items.clear()

        for item in items:
            if isinstance(item, Application):
                widget = LauncherAppItem(item, self.scale)
            else:
                widget = item
            self._list_box.append(widget)
            self._added_items.append(widget)

        height = min(len(items) * 75 + 90, 500) * self.scale
        self._animate_height(height)

        if reset_index:
            self.active_index = 0
        self._update_active_style()

    def set_visible(self, value: bool):
        if value:
            self.__on_open()
        return super().set_visible(value)

    def _animate_height(self, target_height: float, duration=0.25):
        start_height = self._box.get_allocated_height()
        start_time = GLib.get_monotonic_time()

        def update():
            elapsed = (GLib.get_monotonic_time() - start_time) / 1_000_000
            t = min(elapsed / duration, 1.0)
            t_smooth = 1 - pow(1 - t, 3)
            new_height = round(start_height + (target_height - start_height) * t_smooth)
            self._inner.set_size_request(-1, new_height)
            if t < 1.0:
                return True
            else:
                return False

        GLib.idle_add(update)

    def __on_accept(self, *_):
        if not self._added_items:
            return

        item = self._added_items[self.active_index]
        if isinstance(item, ActionItem) and "clipboard" in item.action.name.lower():
            self.mode = LauncherMode.CLIPBOARD
            self._entry.text = ""
            self._refresh_items()
            return
        if hasattr(item, "launch"):
            item.launch()

        def clear(*_: Any):
            self._entry.text = ""
            for item in self._added_items:
                self._list_box.remove(item)
            self._added_items.clear()
            self.current_items.clear()
            self.mode = LauncherMode.APPLICATIONS
            self._refresh_items()

        GLib.timeout_add(500, clear)

    def _move_active(self, delta: int):
        if not self._added_items:
            return

        self.active_index = max(
            0, min(self.active_index + delta, len(self._added_items) - 1)
        )

        self._update_active_style()
        self._scroll_to_active()

    def _scroll_to_active(self):
        if not self._added_items:
            return

        active_widget = self._added_items[self.active_index]
        ggtk_scrolled = self._scroll_app
        vadj = ggtk_scrolled.get_vadjustment()
        alloc = active_widget.get_allocation()
        y = alloc.y
        vadj.set_value(y)

    def _update_active_style(self):
        for i, item in enumerate(self._added_items):
            if i == self.active_index:
                item.add_css_class("active")
            else:
                item.remove_css_class("active")

    def __search(self, *_):
        query: str = self._entry.text.lower().strip()
        prefix = user.command_prefix
        if self.mode not in [LauncherMode.APPLICATIONS, LauncherMode.CLIPBOARD]:
            self.mode = LauncherMode.APPLICATIONS

        if not query:
            self._refresh_items()
            return

        if query.startswith(prefix):
            self.mode = LauncherMode.ACTIONS

        match self.mode:
            case LauncherMode.APPLICATIONS:
                filtered = self.applications.search(self.applications.apps, query)
                if filtered:
                    self.current_items = filtered[: self.MAX_ITEMS]
                    self._populate_box(self.current_items)
                else:
                    web_btn = SearchWebButton(query, self.scale)
                    self.current_items = [web_btn]
                    self._populate_box([web_btn])

            case LauncherMode.ACTIONS:
                filtered = [
                    ActionItem(action, self.scale)
                    for action in self.actions
                    if query.replace(prefix, "") in action.name.lower().strip()
                ]
                self.current_items = filtered
                self._populate_box(filtered)

            case LauncherMode.CLIPBOARD:
                clipboard_items = get_clipboard_history()
                filtered = [
                    ClipboardItemButton(c, self.scale)
                    for c in clipboard_items
                    if query in c.raw.lower()
                ]
                self.current_items = filtered
                self._populate_box(filtered)

            case _:
                self._refresh_items()
