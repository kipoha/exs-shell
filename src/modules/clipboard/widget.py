import subprocess
from typing import Any

from ignis import widgets, utils

from gi.repository import GLib, GdkPixbuf  # type: ignore

from base.window.animated import AnimatedWindowPopup

from utils.clipboard import get_clipboard_history

from config import config


class ClipboardManager(AnimatedWindowPopup):
    def __init__(
        self,
        animation_duration: int = 300,
        **kwargs: Any,
    ):
        self.buffers = get_clipboard_history()
        self._entry = widgets.Entry(
            placeholder_text="Search", on_change=..., on_accept=...
        )
        self.buffers_scrolled = widgets.Scroll(
            vertical=True,
            child=[]
        )
        super().__init__(
            namespace=f"{config.NAMESPACE}_clipboard",
            layer="top",
            anchor=["bottom"],
            kb_mode="on_demand",
            animation_duration=animation_duration,
            **kwargs,
        )

    def refresh(self):
        self._main_box.remove_all_children()
        for buffer_data in self.buffers:
            self._main_box.add_child(self.create_button(buffer_data))

    async def create_button(self, buffer_data: dict):
        buffer_id = buffer_data["id"]
        raw_text = buffer_data["raw"]
        is_binary = buffer_data["is_binary"]

        if is_binary:
            image_bytes = utils.exec_sh_async(f"cliphist decode {buffer_id}")

            loader = GdkPixbuf.PixbufLoader.new()
            loader.write(image_bytes)
            loader.close()
            pixbuf = loader.get_pixbuf()

            target_height = 80
            original_width = pixbuf.get_width()
            original_height = pixbuf.get_height()
            target_width = int(original_width * (target_height / original_height))

            pixbuf = pixbuf.scale_simple(
                target_width, target_height, GdkPixbuf.InterpType.BILINEAR
            )

            image = widgets.Picture(
                pixbuf=pixbuf,
                width=target_width,
                height=target_height,
                content_fit="cover",
            )
            box = widgets.Box(spacing=6, child=image, hexpand=True)

        else:
            label = widgets.Label(label=raw_text.split("\t", 1)[-1])
            box = widgets.Box(spacing=6, child=label, hexpand=True)

        def on_click(*_):
            self.animate_hide()
            proc = subprocess.Popen(
                ["cliphist", "decode", str(buffer_id)], stdout=subprocess.PIPE
            )
            subprocess.run(["wl-copy"], stdin=proc.stdout)
            proc.stdout.close()  # type: ignore
            proc.wait()

            GLib.timeout_add(500, lambda: self.__search.set_text("") or False)

        btn = widgets.Button(child=box, on_click=on_click)
        return btn

    def open(self):
        self.buffers = get_clipboard_history()
        return super().open()
