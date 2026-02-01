from typing import Any
from ignis import widgets

from gi.repository import Gtk, Gdk, GLib  # type: ignore

from exs_shell_deprecated.utils.lock import locked


class BaseAnimatedWindow(widgets.Window):
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
        **kwargs: Any,
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
            **kwargs,
        )

    def open(self):
        if not hasattr(self, "_main_box"):
            raise NotImplementedError("You need to implement _main_box")

        if not self._is_open:
            self.set_visible(True)
            self._main_box.remove_css_class("hidden")
            self._main_box.add_css_class("visible")
            self._is_open = True

    def close(self):
        if not hasattr(self, "_main_box"):
            raise NotImplementedError("You need to implement _main_box")

        if self._is_open:
            self._main_box.remove_css_class("visible")
            self._main_box.add_css_class("hidden")

            def hide_after_animation():
                self._is_open = False
                self.set_visible(False)
                return False

            GLib.timeout_add(self.animation_duration + 50, hide_after_animation)

    def toggle(self):
        if not self._is_open:
            self.open()
        else:
            self.close()


class AnimatedWindow(BaseAnimatedWindow):
    def open(self):
        if not locked():
            return super().open()


class PartiallyAnimatedWindow(AnimatedWindow):
    def open(self):
        if not locked():
            if self._is_open:
                return

            self.set_visible(True)
            self._is_open = True

            if hasattr(self, "_animated_parts") and self._animated_parts:
                for widget in self._animated_parts:
                    self._animate_show(widget)
            else:
                self._animate_show(self._main_box)

    def close(self):
        if not self._is_open:
            return

        if hasattr(self, "_animated_parts") and self._animated_parts:
            for widget in self._animated_parts:
                self._animate_hide(widget)
        else:
            self._animate_hide(self._main_box)

        GLib.timeout_add(self.animation_duration + 50, self._final_hide)

    def _animate_show(self, widget):
        ctx = widget.get_style_context()
        ctx.remove_class("hidden")
        ctx.add_class("visible")
        return False

    def _animate_hide(self, widget):
        ctx = widget.get_style_context()
        ctx.remove_class("visible")
        ctx.add_class("hidden")
        return False

    def _final_hide(self):
        self.set_visible(False)
        self._is_open = False
        return False


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
        **kwargs: Any,
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
            **kwargs,
        )

        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self._on_key_press)
        self.add_controller(key_controller)

    def open(self):
        if not locked():
            if not self._is_open:
                super().open()
                self.focus()

    def focus(self):
        if hasattr(self, "_entry"):
            self._entry.grab_focus()
        else:
            self.grab_focus()

    def _on_key_press(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape and self._is_open:
            self.toggle()
            return True
        return False
