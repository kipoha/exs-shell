import os
import shutil
import asyncio

from ignis import utils
from ignis.base_service import BaseService
from ignis.services.wallpaper.window import (
    WallpaperLayerWindow as WallpaperLayerWindowBase,
)

from exs_shell.base.singleton import SingletonClass
from exs_shell.config.user import options
from exs_shell.config.log import logger
from exs_shell.utils.load_scss import build_scss
from exs_shell.utils.path import Dirs

_OLD_CACHE_WALLPAPER_PATH = f"{Dirs.CACHE_DIR}/wallpaper"
CACHE_WALLPAPER_PATH = f"{Dirs.DATA_DIR}/wallpaper"

if not os.path.exists(CACHE_WALLPAPER_PATH) and os.path.exists(
    _OLD_CACHE_WALLPAPER_PATH
):
    logger.warning(
        f"Copying the cached wallpaper to the new directory: {_OLD_CACHE_WALLPAPER_PATH} -> {CACHE_WALLPAPER_PATH}"
    )
    shutil.copy(_OLD_CACHE_WALLPAPER_PATH, CACHE_WALLPAPER_PATH)


class Wallpaper(SingletonClass):
    def __init__(self):
        options.wallpaper.connect_option("wallpaper_path", self.__set_wallpaper)

    def __set_wallpaper(self):
        path = options.wallpaper.wallpaper_path
        build_scss(path)
        asyncio.create_task(utils.exec_sh_async(f"swww img {path}"))


class WallpaperLayerWindow(WallpaperLayerWindowBase):
    pass


class WallpaperService(BaseService):
    """
    A simple service to set the wallpaper.
    Supports multiple monitors.

    There are options available for this service: :class:`~ignis.options.Options.Wallpaper`.

    Example usage:

    .. code-block:: python

        .. code-block:: python

        from ignis.services.wallpaper import WallpaperService
        from ignis.options import options

        WallpaperService.get_default()  # just to initialize it

        options.wallpaper.set_wallpaper_path("path/to/image")
    """

    def __init__(self):
        super().__init__()
        self._windows: list[WallpaperLayerWindow] = []
        options.wallpaper.connect_option(
            "wallpaper_path", lambda: self.__update_wallpaper()
        )
        self.__sync()

    def __update_wallpaper(self) -> None:
        try:
            if options.wallpaper.wallpaper_path is not None:
                shutil.copyfile(options.wallpaper.wallpaper_path, CACHE_WALLPAPER_PATH)
        except shutil.SameFileError:
            return

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
