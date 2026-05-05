import os
import re
import sys

from exs_shell.app.path import Paths, Dirs
from exs_shell.interfaces.types import AnyDict


def get_hex_color() -> AnyDict:
    scss_file = Paths.generate_path("colors.scss", Dirs.CONFIG_DIR)
    if not os.path.exists(scss_file) or "--dev" in sys.argv:
        scss_file = Paths.generate_path("styles/colors.scss", Paths.path)
    variables: AnyDict = {}
    with open(scss_file, "r") as f:
        for line in f:
            m = re.match(r"\s*\$(\w+):\s*(.+?);", line)
            if m:
                var_name, value = m.groups()
                variables[var_name] = value
    return variables
