from typing import Any
from ignis import widgets

from gi.repository import Gtk, Gdk, GLib  # type: ignore

class AnimatedWindow(widgets.Window):
    def __init__(
        self,
        namespace: str,
        monitor: int | None = None,
        anchor: list[str] | None = None,
        exclusivity: str = "normal",
        layer: str = "top",
        kb_mode: str = "none",
        popup: bool = False,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        dynamic_input_region: bool = False,
        animation_duration: int = 300,
        **kwargs: Any
    ):
        self._is_open = False
        self.animation_duration = animation_duration
        super().__init__(
            namespace=namespace,
            monitor=monitor,
            anchor=anchor,
            exclusivity=exclusivity,
            layer=layer,
            kb_mode=kb_mode,
            popup=popup,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            dynamic_input_region=dynamic_input_region,
            **kwargs
        )

    def open(self):
        if not self._is_open:
            self.set_visible(True)
            self._main_box.remove_css_class("hidden")
            self._main_box.add_css_class("visible")
            self._is_open = True

    def close(self):
        if self._is_open:
            self._main_box.remove_css_class("visible")
            self._main_box.add_css_class("hidden")

            def hide_after_animation():
                self._is_open = False
                self.set_visible(False)
                return False

            GLib.timeout_add(self.animation_duration, hide_after_animation)

    def toggle(self):
        if not hasattr(self, "_main_box"):
            raise NotImplementedError("You need to implement _main_box")

        if not self._is_open:
            self.open()
        else:
            self.close()


class AnimatedWindowPopup(AnimatedWindow):
    def __init__(
        self,
        namespace: str,
        monitor: int | None = None,
        anchor: list[str] | None = None,
        exclusivity: str = "normal",
        layer: str = "top",
        kb_mode: str = "none",
        popup: bool = False,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        dynamic_input_region: bool = False,
        animation_duration: int = 300,
        **kwargs: Any
    ):
        self.animation_duration = animation_duration

        super().__init__(
            namespace=namespace,
            monitor=monitor,
            anchor=anchor,
            exclusivity=exclusivity,
            layer=layer,
            kb_mode=kb_mode,
            popup=popup,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            dynamic_input_region=dynamic_input_region,
            animation_duration=animation_duration,
            **kwargs
        )

        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.__on_key_press)
        self.add_controller(key_controller)

    def open(self):
        if not self._is_open:
            super().open()
            self.focus()

    def focus(self):
        if hasattr(self, "_entry"):
            self._entry.grab_focus()
        else:
            self.grab_focus()

    def __on_key_press(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape and self._is_open:
            self.toggle()
            return True
        return False
