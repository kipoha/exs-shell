from pathlib import Path
from typing import Iterable

from loguru import logger

from ignis import utils
from ignis.css_manager import CssInfoPath, CssManager

from exs_shell.app.vars import NAME
from exs_shell.utils.load_scss import build_scss
from exs_shell.utils.path import Paths


def set_css_file(css_manager, css_file_path: str | Path | Iterable[str | Path]) -> None:
    if isinstance(css_file_path, (str, Path)):
        file = css_file_path
    else:
        css_file_path = list(css_file_path)
        file = css_file_path[-1] if css_file_path else None

    if not file:
        logger.error("Empty css file path")
        exit(1)

    if Path(file).suffix != ".scss":
        logger.error("File must be a scss file")
        exit(1)

    css_manager.apply_css(
        CssInfoPath(
            name=NAME,
            compiler_function=lambda path: utils.sass_compile(path),
            path=Paths.generate_path(file),
        )
    )


def init(css_manager: CssManager, debug: bool) -> None:
    scss = Paths.generate_path("styles/main.scss")
    if not debug:
        scss = build_scss()
    set_css_file(css_manager, scss)
