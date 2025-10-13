import os
import pam
import getpass

from ignis import widgets
from ignis.window_manager import WindowManager

from gi.repository import Gtk  # type: ignore

from config import config

window_manager = WindowManager.get_default()


class LockScreen(widgets.Window):
    def __init__(self):
        self._entry = widgets.Entry(
            placeholder_text="Password",
            hexpand=False,
            visibility=False,
            css_classes=["lockscreen-entry"],
            on_accept=self.__on_accept,
        )

        self._label = widgets.Label(
            label="Lockscreen",
            css_classes=["lockscreen-label"],
        )

        main_box = widgets.Box(
            vertical=True,
            halign="center",
            valign="center",
            spacing=16,
            child=[self._label, self._entry],
        )

        super().__init__(
            namespace=f"{config.NAMESPACE}_lockscreen",
            visible=False,
            popup=True,
            kb_mode="exclusive",
            css_classes=["lockscreen-window"],
            anchor=["top", "right", "bottom", "left"],
            child=widgets.Overlay(
                child=widgets.Button(
                    vexpand=True,
                    hexpand=True,
                    can_focus=False,
                    on_click=lambda _: None,
                ),
                overlays=[main_box],
            ),
            setup=lambda self: self.connect("notify::visible", self.__on_open),
        )

        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.__on_key_press)
        self.add_controller(key_controller)

    def __on_open(self, *args):
        if not self.visible:
            return
        self._entry.set_text("")
        self._entry.grab_focus()

    def __on_key_press(self, controller, keyval, keycode, state):
        if self._entry.has_focus():
            return False
        return True

    def __on_accept(self, *args):
        username = os.getenv("USER") or getpass.getuser()
        password = self._entry.text.strip()
        print(f"{username}:{password}")

        auth = pam.pam()
        print("AUTHENTICATING")
        authenticated: bool = auth.authenticate(
            username=username,
            password=password,
        )
        print(authenticated)
        if authenticated:
            print("AUTHENTICATED")
            self.set_visible(False)
        else:
            print("EXITING")
            self._entry.set_text("")
