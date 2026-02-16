import json
from pathlib import Path

from dataclasses import asdict

from exs_shell.configs.user import appearance
from exs_shell.interfaces.enums.colorschemes import ColorSchemes
from exs_shell.utils.colorscheme import generate
from exs_shell.utils.path import Dirs, Paths


def build_scss(wallpaper_path: str | None = appearance.wallpaper_path) -> Path:
    theme = generate(
        wallpaper_path=wallpaper_path,
        scheme=ColorSchemes(appearance.scheme_variant),
        dark=appearance.dark,
        contrast=appearance.contrast,
    )
    colors = asdict(theme.colors)

    scss_colors_json_file = Dirs.CONFIG_DIR / "colors.json"
    scss_colors_json_file.write_text(
        json.dumps(colors, sort_keys=True, indent=2, separators=(",", ": "))
    )
    scss_colors_file = Dirs.CONFIG_DIR / "colors.scss"
    scss_colors_file.write_text(theme.scss)
    imports = [
        scss
        for scss in (Paths.path / "styles").glob("**/*.scss")
        if scss.name not in ("main.scss", "colors.scss")
    ]
    imports_text = "\n".join(f'@import "{scss}";' for scss in imports)

    main_scss_file = Dirs.CONFIG_DIR / "main.scss"
    main_scss_file.write_text(f"""@use \"{scss_colors_file}\" as c;

{imports_text}

* {{
  all: unset;
  font-family: JetBrainsMono;
  font-weight: bold;
  transition: background-color 0.1s ease, opacity 0.25s ease, transform 0.25s ease;
}}""")

    return main_scss_file
