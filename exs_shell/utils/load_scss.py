import json
from pathlib import Path

from dataclasses import asdict

from exs_shell.configs.user import options
from exs_shell.utils.colors.utils import generate_theme
from exs_shell.utils.path import Dirs, Paths


def build_scss(wallpaper_path: str | None = options.appearance.wallpaper_path) -> Path:
    colors, _ = generate_theme(wallpaper_path=wallpaper_path)
    colors = asdict(colors)

    scss_colors_json_file = Dirs.CONFIG_DIR / "colors.json"
    scss_colors_json_file.write_text(
        json.dumps(colors, sort_keys=True, indent=2, separators=(",", ": "))
    )
    lines = [f"${k}: {v};" for k, v in colors.items()]
    scss_colors_file = Dirs.CONFIG_DIR / "colors.scss"
    scss_colors_file.write_text("\n".join(lines))
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
