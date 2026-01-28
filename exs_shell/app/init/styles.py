from loguru import logger

from ignis import utils
from ignis.css_manager import CssInfoPath, CssManager

from exs_shell.app.vars import NAME
from exs_shell.utils.load_scss import build_scss
from exs_shell.utils.path import Paths


def set_css_file(css_manager: CssManager, css_file_path: str | list[str]) -> None:
    file = (
        css_file_path
        if isinstance(css_file_path, str)
        else css_file_path[-1]
        if len(css_file_path) > 0
        else ""
    )
    if file.split(".")[-1] != "scss":
        logger.error("File must be a scss file")
        exit(1)

    css_manager.apply_css(
        CssInfoPath(
            name=NAME,
            compiler_function=lambda path: utils.sass_compile(path),
            path=Paths.generate_path(css_file_path),
        )
    )


def init(css_manager: CssManager, debug: bool) -> None:
    scss = Paths.generate_path("styles/main.scss")
    if not debug:
        scss = build_scss()
    set_css_file(css_manager, scss)
