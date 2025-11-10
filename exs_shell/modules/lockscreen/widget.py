import os
import pam
import getpass

from ignis import widgets

from gi.repository import Gtk  # type: ignore

from exs_shell.config import config
from exs_shell.config.user import options
from exs_shell.base.window.animated import BaseAnimatedWindow


class LockScreen(BaseAnimatedWindow):
    def __init__(self, monitor: int = 0):
        self._entry = widgets.Entry(
            placeholder_text="Password",
            hexpand=False,
            visibility=False,
            css_classes=["lockscreen-entry"],
            on_accept=self.__on_accept,
        )

        self._entry.connect("changed", self.__on_entry_changed)

        self._entry_box = widgets.Box(
            css_classes=["lockscreen-entry-box"],
            child=[self._entry],
            halign="fill",
            hexpand=True,
            valign="center",
        )

        self._left_entry_corner = widgets.Corner(
            css_classes=["lockscreen-left-entry-corner"],
            orientation="bottom-right",
            width_request=50,
            height_request=70,
            halign="end",
            valign="end",
        )

        self._right_entry_corner = widgets.Corner(
            css_classes=["lockscreen-right-entry-corner"],
            orientation="bottom-left",
            width_request=50,
            height_request=70,
            halign="start",
            valign="end",
        )

        self._entry_container = widgets.Box(
            css_classes=["lockscreen-entry-container"],
            halign="center",
            valign="end",
            child=[
                self._left_entry_corner,
                self._entry_box,
                self._right_entry_corner,
            ],
        )

        self._bg_image = widgets.Picture(
            css_classes=["lockscreen-bg"],
            content_fit="cover",
            image=options.wallpaper.bind("wallpaper_path"),
        )
        self._root_bg = widgets.Picture(
            css_classes=["lockscreen-bg-root"],
            content_fit="cover",
            image=options.wallpaper.bind("wallpaper_path"),
        )
        self._main_box = widgets.Box(
            vertical=True,
            css_classes=["lockscreen-window"],
            child=[
                widgets.Box(vexpand=True, hexpand=True),
                self._entry_container,
            ],
        )
        self._overlay = widgets.Overlay(child=self._bg_image)
        self._overlay.add_overlay(self._main_box)
        self._root_overlay = widgets.Overlay(child=self._root_bg)
        self._root_overlay.add_overlay(self._overlay)

        super().__init__(
            namespace=f"{config.NAMESPACE}_lockscreen_{monitor}",
            monitor=monitor,
            visible=False,
            popup=True,
            hexpand=True,
            vexpand=True,
            kb_mode="exclusive",
            anchor=["top", "right", "bottom", "left"],
            # child=self._main_box,
            # child=self._overlay,
            child=self._root_overlay,
        )

        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.__on_key_press)
        self.add_controller(key_controller)

    def open(self):
        self._entry.set_text("")
        self._entry.grab_focus()
        self._bg_image.add_css_class("visible")
        self._bg_image.remove_css_class("hidden")
        self._root_bg.add_css_class("visible")
        self._root_bg.remove_css_class("hidden")
        return super().open()

    def close(self):
        self._bg_image.add_css_class("hidden")
        self._bg_image.remove_css_class("visible")
        self._root_bg.add_css_class("hidden")
        self._root_bg.remove_css_class("visible")
        return super().close()

    def __on_key_press(self, controller, keyval, keycode, state):
        if self._entry.has_focus():
            return False
        return True

    def __on_entry_changed(self, entry):
        text = entry.get_text().strip()
        if text:
            self._entry_box.remove_css_class("hidden")
            self._entry_box.add_css_class("visible")
            self._left_entry_corner.remove_css_class("hidden")
            self._right_entry_corner.remove_css_class("hidden")
            self._left_entry_corner.add_css_class("visible")
            self._right_entry_corner.add_css_class("visible")
        else:
            self._entry_box.remove_css_class("visible")
            self._entry_box.add_css_class("hidden")
            self._left_entry_corner.remove_css_class("visible")
            self._right_entry_corner.remove_css_class("visible")
            self._left_entry_corner.add_css_class("hidden")
            self._right_entry_corner.add_css_class("hidden")

    def __on_accept(self, *args):
        username = os.getenv("USER") or getpass.getuser()
        password = self._entry.text.strip()

        auth = pam.pam()
        authenticated: bool = auth.authenticate(
            username=username,
            password=password,
        )
        if authenticated:
            self.close()
            self._entry_box.remove_css_class("visible")
            self._entry_box.add_css_class("hidden")
            self._left_entry_corner.remove_css_class("visible")
            self._right_entry_corner.remove_css_class("visible")
            self._left_entry_corner.add_css_class("hidden")
            self._right_entry_corner.add_css_class("hidden")
        else:
            self._entry.set_text("")
