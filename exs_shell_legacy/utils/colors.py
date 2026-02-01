import os
import re

from exs_shell_deprecated.utils.path import PathUtils, Dirs


def get_hex_color() -> str:
    scss_file = PathUtils.generate_path("colors.scss", Dirs.CONFIG_DIR)
    if not os.path.exists(scss_file):
        scss_file = PathUtils.generate_path("styles/colors.scss", PathUtils.path)
    variables = {}
    with open(scss_file, "r") as f:
        for line in f:
            m = re.match(r"\s*\$(\w+):\s*(.+?);", line)
            if m:
                var_name, value = m.groups()
                variables[var_name] = value
    return variables["accent"]


def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return r, g, b
