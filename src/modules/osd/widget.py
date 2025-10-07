import subprocess

from gi.repository import GLib  # type: ignore

from ignis import widgets, utils

from config import config


class OSDProgress(widgets.Box):
    def __init__(self, icon: str, name: str):
        super().__init__(vertical=False, halign="center", valign="center", spacing=20)
        self._name = name
        self._icon_active = icon
        self._icon_muted = "" if name == "volume" else icon
        self._label = widgets.Label(label=icon, css_classes=[f"{name}-icon"])
        self._bar = widgets.Scale(
            orientation="horizontal",
            min=0,
            max=100,
            value=0,
            css_classes=[f"{name}-bar"],
        )
        self._bar.set_sensitive(False)

        self._current_value = 0
        self._target_value = 0
        self._anim_source = None
        self._muted = False

        self.append(self._label)
        self.append(self._bar)

    def update(self, value: int):
        self._target_value = max(0, min(100, value))
        if self._anim_source is None:
            self._anim_source = GLib.timeout_add(10, self._animate_step)

    def _animate_step(self):
        diff = self._target_value - self._current_value
        if abs(diff) < 1:
            self._current_value = self._target_value
            self._bar.set_value(self._current_value)
            self._anim_source = None
            return False
        self._current_value += diff * 0.2
        self._bar.set_value(self._current_value)
        return True

    def set_muted(self, muted: bool):
        self._muted = muted
        self._label.set_label(self._icon_muted if muted else self._icon_active)


class OSD(widgets.Window):
    def __init__(self, **kwargs):
        super().__init__(
            namespace=f"{config.NAMESPACE}_osd",
            popup=True,
            layer="overlay",
            visible=False,
            anchor=["bottom"],
            **kwargs,
        )

        self._hide_timeout = None
        self._last_device = None

        self._volume_value = self.get_volume()
        self._brightness_value = self.get_brightness()

        self._volume_widget = OSDProgress("", "volume")
        self._brightness_widget = OSDProgress("󰃞", "brightness")

        self._box = widgets.Box(
            vertical=True,
            spacing=12,
            halign="center",
            valign="center",
            css_classes=["osd-container", "hidden"],
            child=[self._brightness_widget, self._volume_widget],
        )

        self.set_child(self._box)

        self._volume_widget.update(self._volume_value)
        self._brightness_widget.update(self._brightness_value)

        self._start_device_monitor()

    def get_volume(self) -> int:
        try:
            result = subprocess.run(
                ["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"],
                capture_output=True,
                text=True,
            )
            parts = result.stdout.strip().split()
            return int(float(parts[1]) * 100) if len(parts) > 1 else 0
        except Exception:
            return 0

    def get_brightness(self) -> int:
        try:
            bright = int(
                subprocess.run(
                    ["brightnessctl", "get"], capture_output=True, text=True
                ).stdout.strip()
            )
            max_bright = int(
                subprocess.run(
                    ["brightnessctl", "max"], capture_output=True, text=True
                ).stdout.strip()
            )
            return int(bright * 100 / max_bright)
        except Exception:
            return 0

    def show_osd(self):
        if not self.visible:
            self.visible = True

        self._box.remove_css_class("hidden")
        self._box.add_css_class("visible")

        if self._hide_timeout:
            try:
                GLib.source_remove(self._hide_timeout)
            except Exception:
                pass

        self._hide_timeout = GLib.timeout_add_seconds(1, self.hide_osd)

    def hide_osd(self):
        self._box.remove_css_class("visible")
        self._box.add_css_class("hidden")

        def hide_window():
            self.visible = False

        utils.Timeout(300, hide_window)
        self._hide_timeout = None
        return False

    def update_volume(self, up: bool = True):
        step = 5 if up else -5
        self._volume_value = max(0, min(100, self._volume_value + step))
        subprocess.Popen(
            ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{self._volume_value / 100.0}"]
        )
        self._volume_widget.update(self._volume_value)
        self.show_osd()

    def toggle_mute(self):
        subprocess.Popen(["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"])
        GLib.timeout_add(100, self._update_mute_state)
        self.show_osd()

    def _update_mute_state(self):
        try:
            out = subprocess.check_output(["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"], text=True)
            self._volume_widget.set_muted("MUTED" in out)
        except Exception:
            pass
        return False

    def update_brightness(self, up: bool = True):
        step = 5 if up else -5
        self._brightness_value = max(1, min(100, self._brightness_value + step))
        subprocess.Popen(["brightnessctl", "set", f"{self._brightness_value}%"])
        self._brightness_widget.update(self._brightness_value)
        self.show_osd()

    def _start_device_monitor(self):
        self._last_device = None

        def poll_device():
            try:
                out = subprocess.check_output(["pactl", "info"], text=True)
                for line in out.splitlines():
                    if line.startswith("Default Sink:"):
                        device = line.split(":", 1)[1].strip()
                        if device != self._last_device:
                            self._last_device = device
                            self._volume_value = self.get_volume()
                            self._volume_widget.update(self._volume_value)
                            self.show_osd()
                        break
            except Exception:
                pass
            return True

        GLib.timeout_add_seconds(2, poll_device)
