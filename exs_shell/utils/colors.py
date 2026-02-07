import os
import re

from exs_shell.interfaces.types import AnyDict
from exs_shell.utils.path import Paths, Dirs


def get_hex_color() -> AnyDict:
    scss_file = Paths.generate_path("colors.scss", Dirs.CONFIG_DIR)
    if not os.path.exists(scss_file):
        scss_file = Paths.generate_path("styles/colors.scss", Paths.path)
    variables: AnyDict = {}
    with open(scss_file, "r") as f:
        for line in f:
            m = re.match(r"\s*\$(\w+):\s*(.+?);", line)
            if m:
                var_name, value = m.groups()
                variables[var_name] = value
    return variables


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return r, g, b
