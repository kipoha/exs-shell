import subprocess

from typing import Any

from gi.repository import GLib, GdkPixbuf  # type: ignore

from ignis import widgets
from ignis.window_manager import WindowManager

from exs_shell_deprecated.base.singleton import SingletonClass
from exs_shell_deprecated.base.window.animated import PartiallyAnimatedWindow, AnimatedWindowPopup

from exs_shell_deprecated.utils.clipboard import get_clipboard_history
from exs_shell_deprecated.config import config

window_manager = WindowManager.get_default()


class ClipboardManager(PartiallyAnimatedWindow, AnimatedWindowPopup, SingletonClass):
    def __init__(self):
        self.MAX_ITEMS = 10

        self.current_items = get_clipboard_history()[: self.MAX_ITEMS]

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
                widgets.Box(css_classes=["launcher-search-box"], child=[self._entry]),
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
            namespace=f"{config.NAMESPACE}_clipboard",
            visible=False,
            kb_mode="on_demand",
            anchor=["bottom"],
            child=widgets.Box(
                css_classes=["launcher-overlay"],
                child=[self._background_button, self._main_box],
            ),
        )

        self._added_items = []
        self._populate_box(self.current_items)

    def _populate_box(self, items: list[Any]):
        for item in self._added_items:
            self._list_box.remove(item)
        self._added_items.clear()

        for buffer_data in items:
            widget = self._create_buffer_widget(buffer_data)
            self._list_box.append(widget)
            self._added_items.append(widget)

        height = min(len(items) * 40 + 50, 500)
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

    def _create_buffer_widget(self, buffer_data: dict):
        buffer_id = buffer_data["id"]
        raw_text = buffer_data["raw"]
        is_binary = buffer_data.get("is_binary", False)

        if is_binary:
            try:
                image_bytes = subprocess.run(
                    ["cliphist", "decode", str(buffer_id)], capture_output=True
                ).stdout
                loader = GdkPixbuf.PixbufLoader.new()
                loader.write(image_bytes)
                loader.close()
                pixbuf = loader.get_pixbuf()
                target_height = 80
                scale = target_height / pixbuf.get_height()
                pixbuf = pixbuf.scale_simple(
                    int(pixbuf.get_width() * scale),
                    target_height,
                    GdkPixbuf.InterpType.BILINEAR,
                )
                image = widgets.Picture(
                    image=pixbuf,
                    width=pixbuf.get_width(),
                    height=target_height,
                    content_fit="cover",
                    css_classes=["clipboard-image"],
                )
                box = widgets.Box(spacing=6, child=[image], hexpand=True)
            except Exception as e:
                print(e)
                box = widgets.Box(
                    spacing=6, child=[widgets.Label(label="[image]")], hexpand=True
                )
        else:
            text = raw_text.split("\t")[-1]
            if len(text) > 60:
                text = text[:57] + "..."
            label = widgets.Label(label=text)
            box = widgets.Box(spacing=6, child=[label], hexpand=True)

        btn = widgets.Button(child=box, css_classes=["launcher-app", "clipboard-item"])

        def on_click(*_):
            proc = subprocess.Popen(
                ["cliphist", "decode", str(buffer_id)], stdout=subprocess.PIPE
            )
            subprocess.run(["wl-copy"], stdin=proc.stdout)
            proc.stdout.close()  # type: ignore
            proc.wait()
            self.close()
            GLib.timeout_add(500, lambda: self._entry.set_text("") or False)

        btn.connect("clicked", on_click)
        return btn

    def open(self):
        window_manager.get_window(f"{config.NAMESPACE}_launcher").close()
        window_manager.get_window(f"{config.NAMESPACE}_notification").close()
        self.current_items = get_clipboard_history()[: self.MAX_ITEMS]
        self._populate_box(self.current_items)
        super().open()
        self.__on_open()

    def __on_open(self):
        if not self.visible:
            return
        self._entry.text = ""
        self._entry.grab_focus()

    def __on_accept(self, *_):
        if self._added_items:
            self._added_items[0].child.on_click()

    def __search(self, *_):
        query = self._entry.text.lower().strip()
        if not query:
            self.current_items = get_clipboard_history()[: self.MAX_ITEMS]
            self._populate_box(self.current_items)
            return

        filtered = [b for b in get_clipboard_history() if query in b["raw"].lower()]
        self.current_items = filtered[: self.MAX_ITEMS]
        self._populate_box(self.current_items)
