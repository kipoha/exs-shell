import os
import pam
import getpass
import subprocess

from ignis import utils, widgets

from gi.repository import Gtk, GdkPixbuf, Gdk  # type: ignore

from exs_shell.config import config
from exs_shell.config.user import options
from exs_shell.base.window.animated import BaseAnimatedWindow
from exs_shell.modules.shared.widgets.top_bar.widget import LockScreenTopBar
from exs_shell.utils.path import PathUtils


class LockScreen(BaseAnimatedWindow):
    def __init__(self, monitor: int = 0):
        self._top_bar = LockScreenTopBar.get_default()
        self._entry = widgets.Entry(
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
            height_request=50,
            halign="end",
            valign="end",
        )

        self._right_entry_corner = widgets.Corner(
            css_classes=["lockscreen-right-entry-corner"],
            orientation="bottom-left",
            width_request=50,
            height_request=50,
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
                self._top_bar,
                widgets.Box(
                    vexpand=True,
                    hexpand=True,
                    halign="center",
                    valign="center",
                    child=[widgets.Box(
                        css_classes=["lockscreen-lock-logo"],
                        child=[widgets.Picture(
                            css_classes=["lockscreen-lock-logo-image"],
                            content_fit="cover",
                            image=PathUtils.generate_path(
                                "icons/action/lock_screen.png", PathUtils.assets_path
                            ),
                            width_request=180,
                            height_request=180,
                        )]
                    )],
                ),
                self._entry_container,
            ],
        )
        self._overlay = widgets.Overlay(child=self._bg_image)
        self._overlay.add_overlay(self._main_box)
        self._root_overlay = widgets.Overlay(child=self._root_bg)
        self._root_overlay.add_overlay(self._overlay)

        self.__animate_objs = [
            self._bg_image,
            self._root_bg,
            self._top_bar.center_box,
            self._top_bar.left_center_corner,
            self._top_bar.right_center_corner,
            self._top_bar.left_right_corner,
            self._top_bar.right_box,
            self._top_bar.right_left_corner,
            self._top_bar.left_box,
            self._top_bar.cava_left,
            self._top_bar.cava_right,
        ]

        super().__init__(
            namespace=f"{config.NAMESPACE}_lockscreen_{monitor}",
            monitor=monitor,
            visible=False,
            popup=True,
            layer="overlay",
            hexpand=True,
            vexpand=True,
            kb_mode="exclusive",
            anchor=["top", "right", "bottom", "left"],
            child=self._root_overlay,
        )

        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.__on_key_press)
        self.add_controller(key_controller)

    def open(self):
        monitor_obj = utils.get_monitor(self.monitor)  # type: ignore
        monitor_name = monitor_obj.get_connector()  # type: ignore
        args = ["grim"]
        if monitor_name:
            args += ["-o", monitor_name]
        args.append("-")
        proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        screenshot_bytes = proc.stdout
        if screenshot_bytes:
            loader = GdkPixbuf.PixbufLoader.new_with_type("png")
            loader.write(screenshot_bytes)
            loader.close()
            pixbuf = loader.get_pixbuf()

            if pixbuf:
                texture = Gdk.Texture.new_for_pixbuf(pixbuf)
                self._bg_image.set_paintable(texture)
                self._root_bg.set_paintable(texture)

        self._entry.set_text("")
        self._entry.grab_focus()
        for obj in self.__animate_objs:
            obj.remove_css_class("hidden")
            obj.add_css_class("visible")
        return super().open()

    def close(self):
        for obj in self.__animate_objs:
            obj.remove_css_class("visible")
            obj.add_css_class("hidden")
        return super().close()

    def __on_key_press(self, controller, keyval, keycode, state):
        if self._entry.has_focus():
            return False
        print(controller, keyval, keycode, state)
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

    @utils.run_in_thread
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
