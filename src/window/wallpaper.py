import asyncio

from ignis import utils

from config.user import options

from base.singleton import SingletonClass


class Wallpaper(SingletonClass):
    def __init__(self):
        options.wallpaper.connect_option("wallpaper_path", self.__set_wallpaper)

    def __set_wallpaper(self, path: str):
        asyncio.create_task(utils.exec_sh_async(f"swww img {path}"))
