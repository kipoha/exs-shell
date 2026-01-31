import asyncio

from ignis import utils

from exs_shell.config.user import options

from exs_shell.base.singleton import SingletonClass
from exs_shell.utils.load_scss import build_scss


class Wallpaper(SingletonClass):
    def __init__(self):
        options.wallpaper.connect_option("wallpaper_path", self.__set_wallpaper)

    def __set_wallpaper(self):
        path = options.wallpaper.wallpaper_path
        build_scss(path)
        asyncio.create_task(utils.exec_sh_async(f"swww img {path}"))
