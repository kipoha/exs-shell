import os
import shutil
import sys

from gi.repository import Gtk, Gdk, GLib, Gtk4LayerShell as GtkLayerShell  # type: ignore

from ignis import utils
from ignis.base_service import BaseService
from ignis.exceptions import LayerShellNotSupportedError
from ignis.widgets.picture import Picture
from ignis.app import IgnisApp

from exs_shell import register
from exs_shell.app.vars import NAMESPACE
from exs_shell.configs.user import appearance
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.ui.widgets.windows import Revealer
from exs_shell.utils.load_scss import build_scss
from exs_shell.utils.loop import run_in_thread
from exs_shell.utils.path import Dirs

CACHE_WALLPAPER_PATH = f"{Dirs.DATA_DIR}/wallpaper"


class WallpaperLayerWindow(Gtk.Window):
    def __init__(
        self, wallpaper_path: str, gdkmonitor: Gdk.Monitor, width: int, height: int
    ) -> None:
        if not GtkLayerShell.is_supported():
            raise LayerShellNotSupportedError()

        app = IgnisApp.get_initialized()

        Gtk.Window.__init__(self, application=app)
        GtkLayerShell.init_for_window(self)

        for anchor in ["LEFT", "RIGHT", "TOP", "BOTTOM"]:
            GtkLayerShell.set_anchor(self, getattr(GtkLayerShell.Edge, anchor), True)

        GtkLayerShell.set_exclusive_zone(self, -1)  # ignore other layers

        GtkLayerShell.set_namespace(
            self, name_space=f"{NAMESPACE}_wallpaper_{gdkmonitor.get_model()}"
        )

        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.BACKGROUND)

        GtkLayerShell.set_monitor(self, gdkmonitor)

        pic = Picture(
            image=wallpaper_path,
            content_fit="cover",
            width=width,
            height=height,
        )
        self.revealer = Revealer(
            pic,
            transition_type=RevealerTransition.CROSSFADE,
            transition_duration=500,
            reveal_child=False,
        )
        self.set_child(self.revealer)
        GLib.idle_add(lambda: self.revealer.set_reveal_child(True))

        self.set_visible(True)

    def unrealize(self) -> None:
        self.revealer.set_reveal_child(False)
        GLib.timeout_add(500, self.destroy)
        super().unrealize()


@register.event
@register.service
class AppearanceService(BaseService):
    def __init__(self):
        super().__init__()
        self._windows: list[WallpaperLayerWindow] = []
        self.__sync()

    @register.events.option(appearance, "dark")
    @register.events.option(appearance, "contrast")
    @register.events.option(appearance, "scheme_variant")
    def __update(self) -> None:
        if "--dev" in sys.argv or "--debug" in sys.argv:
            return
        build_scss(appearance.wallpaper_path)

    @register.events.option(appearance, "wallpaper_path")
    def __update_wallpaper(self) -> None:
        try:
            if appearance.wallpaper_path is not None:
                shutil.copyfile(appearance.wallpaper_path, CACHE_WALLPAPER_PATH)
        except shutil.SameFileError:
            return

        build_scss(appearance.wallpaper_path)

        self.__sync()

    def __sync(self) -> None:
        for i in self._windows:
            i.unrealize()

        if not os.path.isfile(CACHE_WALLPAPER_PATH):
            return

        self._windows = []

        for monitor_id in range(utils.get_n_monitors()):
            gdkmonitor = utils.get_monitor(monitor_id)
            if not gdkmonitor:
                return

            geometry = gdkmonitor.get_geometry()
            window = WallpaperLayerWindow(
                wallpaper_path=CACHE_WALLPAPER_PATH,
                gdkmonitor=gdkmonitor,
                width=geometry.width,
                height=geometry.height,
            )
            self._windows.append(window)
