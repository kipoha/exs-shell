from gi.repository import GdkPixbuf, Gtk, GLib, Gdk  # type: ignore
from ignis.widgets import Box, Picture


def is_animated_gif(path: str) -> bool:
    try:
        anim = GdkPixbuf.PixbufAnimation.new_from_file(path)
        return not anim.is_static_image()
    except Exception:
        return False


class SmartPicture(Box):
    def __init__(self, image: str, width: int, height: int):
        super().__init__()
        self.set_size_request(width, height)
        self._width = width
        self._height = height
        self._timer_id = None
        self._frames: list[tuple[GdkPixbuf.Pixbuf, int]] = []
        self._frame_index = 0
        # self._child = None

        if is_animated_gif(image):
            self._setup_gif(image, width, height)
        else:
            self._setup_static(image)

    def _setup_static(self, path: str):
        child = Picture(
            image=path,
            content_fit="cover",
            width=self._width,
            height=self._height,
        )
        self.append(child)
        self._child = child

    def _setup_gif(self, path: str, width: int, height: int):
        anim = GdkPixbuf.PixbufAnimation.new_from_file(path)
        self._frame_index = 0

        # Извлекаем кадры через SimpleAnim итератор
        # используем get_iter с текущим временем через GLib
        it = anim.get_iter(None)
        first_pixbuf = it.get_pixbuf()
        
        # Считаем scale/offset один раз по первому кадру
        src_w = first_pixbuf.get_width()
        src_h = first_pixbuf.get_height()
        self._scale = max(width / src_w, height / src_h)
        self._off_x = (width - src_w * self._scale) / 2
        self._off_y = (height - src_h * self._scale) / 2

        # Собираем кадры: копируем каждый pixbuf
        max_frames = 256
        while len(self._frames) < max_frames:
            delay = it.get_delay_time()
            if delay <= 0:
                delay = 100
            self._frames.append((it.get_pixbuf().copy(), delay))
            # advance возвращает False когда анимация зациклилась
            try:
                went = it.advance(None)
            except Exception:
                break
            if not went:
                break

        area = Gtk.DrawingArea()
        area.set_content_width(width)
        area.set_content_height(height)
        area.set_draw_func(self._draw_gif)
        self.append(area)
        self._child = area
        self._schedule_frame()

    def _schedule_frame(self):
        if not self._frames:
            return
        _, delay = self._frames[self._frame_index]
        self._timer_id = GLib.timeout_add(delay, self._next_frame)

    def _next_frame(self) -> bool:
        self._frame_index = (self._frame_index + 1) % len(self._frames)
        if self._child:
            self._child.queue_draw()
        self._schedule_frame()
        return False

    def _draw_gif(self, area, cr, width, height):
        if not self._frames:
            return
        pixbuf, _ = self._frames[self._frame_index]
        cr.rectangle(0, 0, width, height)
        cr.clip()
        cr.translate(self._off_x, self._off_y)
        cr.scale(self._scale, self._scale)
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()

    def stop(self):
        """Вызывать при смене обоев перед уничтожением виджета"""
        if self._timer_id is not None:
            GLib.source_remove(self._timer_id)
            self._timer_id = None
        self._frames.clear()
        self._child = None

    def destroy(self):
        self.stop()
        super().destroy()
# from gi.repository import GdkPixbuf, Gtk, GLib, Gdk  # type: ignore
#
# from ignis.widgets import Box, Picture
#
#
# def is_animated_gif(path: str) -> bool:
#     try:
#         anim = GdkPixbuf.PixbufAnimation.new_from_file(path)
#         return not anim.is_static_image()
#     except Exception:
#         return False
#
#
# class SmartPicture(Box):
#     def __init__(self, image: str, width: int, height: int):
#         super().__init__()
#         self.set_size_request(width, height)
#         self._width = width
#         self._height = height
#         self._timer_id = None
#
#         if is_animated_gif(image):
#             self._setup_gif(image, width, height)
#         else:
#             self._setup_static(image)
#
#     def _setup_static(self, path: str):
#         child = Picture(
#             image=path,
#             content_fit="cover",
#             width=self._width,
#             height=self._height,
#         )
#         self.append(child)
#         self._child = child
#
#     # def _setup_gif(self, path: str, width: int, height: int):
#     #     anim = GdkPixbuf.PixbufAnimation.new_from_file(path)
#     #     self._frames: list[tuple[GdkPixbuf.Pixbuf, int]] = []
#     #     self._frame_index = 0
#     #
#     #     it = anim.get_iter(None)
#     #     while True:
#     #         delay = it.get_delay_time()
#     #         if delay < 0:
#     #             delay = 100
#     #
#     #         raw = it.get_pixbuf()
#     #         scaled = self._scale_cover(raw, width, height)
#     #         self._frames.append((scaled, delay))
#     #
#     #         advanced = it.advance(None)
#     #         if not advanced:
#     #             break
#     #         if len(self._frames) > 512:
#     #             break
#     #
#     #     area = Gtk.DrawingArea()
#     #     area.set_content_width(width)
#     #     area.set_content_height(height)
#     #     area.set_draw_func(self._draw_gif)
#     #     self.append(area)
#     #     self._child = area
#     #     self._schedule_frame()
#
#     def _scale_cover(
#         self, pixbuf: GdkPixbuf.Pixbuf, w: int, h: int
#     ) -> GdkPixbuf.Pixbuf:
#         src_w = pixbuf.get_width()
#         src_h = pixbuf.get_height()
#         scale = max(w / src_w, h / src_h)
#         new_w = int(src_w * scale)
#         new_h = int(src_h * scale)
#         return pixbuf.scale_simple(new_w, new_h, GdkPixbuf.InterpType.BILINEAR)
#
#     def _schedule_frame(self):
#         _, delay = self._frames[self._frame_index]
#         self._timer_id = GLib.timeout_add(delay, self._next_frame)
#
#     def _next_frame(self) -> bool:
#         self._frame_index = (self._frame_index + 1) % len(self._frames)
#         self._child.queue_draw()
#         self._schedule_frame()
#         return False
#
#     # def _draw_gif(self, area, cr, width, height):
#     #     pixbuf, _ = self._frames[self._frame_index]
#     #     off_x = (width - pixbuf.get_width()) / 2
#     #     off_y = (height - pixbuf.get_height()) / 2
#     #     cr.rectangle(0, 0, width, height)
#     #     cr.clip()
#     #     Gdk.cairo_set_source_pixbuf(cr, pixbuf, off_x, off_y)
#     #     cr.paint()
#
#     def do_measure(self, orientation, for_size):
#         return self._width, self._width, -1, -1
#
#     def do_size_allocate(self, width, height, baseline):
#         self._child.allocate(width, height, baseline, None)
#
#     def destroy(self):
#         if self._timer_id is not None:
#             GLib.source_remove(self._timer_id)
#             self._timer_id = None
#         super().destroy()
#
#     def _setup_gif(self, path: str, width: int, height: int):
#         anim = GdkPixbuf.PixbufAnimation.new_from_file(path)
#         self._frames: list[tuple[GdkPixbuf.Pixbuf, int]] = []
#         self._frame_index = 0
#         self._scale = 1.0
#         self._off_x = 0.0
#         self._off_y = 0.0
#
#         it = anim.get_iter(None)
#         while True:
#             delay = it.get_delay_time()
#             if delay < 0:
#                 delay = 100
#             # Копируем pixbuf чтобы итератор не перезаписал его
#             self._frames.append((it.get_pixbuf().copy(), delay))
#             if not it.advance(None) or len(self._frames) > 512:
#                 break
#
#         first = self._frames[0][0]
#         src_w, src_h = first.get_width(), first.get_height()
#         self._scale = max(width / src_w, height / src_h)
#         self._off_x = (width - src_w * self._scale) / 2
#         self._off_y = (height - src_h * self._scale) / 2
#
#         area = Gtk.DrawingArea()
#         area.set_content_width(width)
#         area.set_content_height(height)
#         area.set_draw_func(self._draw_gif)
#         self.append(area)
#         self._child = area
#         self._schedule_frame()
#
#     def _draw_gif(self, area, cr, width, height):
#         pixbuf, _ = self._frames[self._frame_index]
#         cr.rectangle(0, 0, width, height)
#         cr.clip()
#         cr.translate(self._off_x, self._off_y)
#         cr.scale(self._scale, self._scale)
#         Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
#         cr.paint()
