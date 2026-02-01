import os
import json

from exs_shell_deprecated.colors.utils import generate_theme
from exs_shell_deprecated.utils.path import Dirs, PathUtils
from exs_shell_deprecated.config.user import options


def build_scss(wallpaper_path: str | None = options.wallpaper.wallpaper_path) -> str:
    colors, _ = generate_theme(wallpaper_path=wallpaper_path)
    if colors is None:
        json_colors_config = PathUtils.generate_path("colors.json", Dirs.CONFIG_DIR)
        if not os.path.exists(json_colors_config):
            json_colors_source = PathUtils.generate_path("colors.json", PathUtils.path)
            with open(json_colors_source, "r") as f:
                source_colors = json.load(f)

            with open(json_colors_config, "w") as f:
                json.dump(source_colors, f, indent=2)

        with open(json_colors_config, "r") as f:
            colors = json.load(f)

    lines = [f"${k}: {v};" for k, v in colors.items()]
    scss_colors = PathUtils.generate_path("colors.scss", Dirs.CONFIG_DIR)
    imports = [
        scss
        for scss in (PathUtils.path / "styles").glob("**/*.scss")
        if scss.name not in ("main.scss", "colors.scss")
    ]
    imports_text = "\n".join(f'@import "{scss}";' for scss in imports)

    with open(scss_colors, "w") as f:
        f.write("\n".join(lines))
    main_scss = PathUtils.generate_path("main.scss", Dirs.CONFIG_DIR)
    with open(main_scss, "w") as f:
        text = f"""@use \"{scss_colors}\" as c;

{imports_text}

* {{
  all: unset;
  font-family: JetBrainsMono;
  font-weight: bold;
  transition: background-color 0.1s ease, opacity 0.25s ease, transform 0.25s ease;
}}"""
        f.write(text)
    return main_scss
