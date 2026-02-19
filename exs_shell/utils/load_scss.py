import json

from dataclasses import asdict

from exs_shell.configs.user import appearance
from exs_shell.interfaces.enums.colorschemes import ColorSchemes
from exs_shell.utils.colorscheme import generate, generate_color_preview
from exs_shell.utils.loop import run_in_thread
from exs_shell.utils.path import Dirs, Paths


@run_in_thread
def build_scss(wallpaper_path: str | None = appearance.wallpaper_path):
    theme = generate(
        wallpaper_path=wallpaper_path,
        scheme=ColorSchemes(appearance.scheme_variant),
        dark=appearance.dark,
        contrast=appearance.contrast,
    )
    colors = asdict(theme.colors)
    preview = generate_color_preview(
        wallpaper_path,  # type: ignore
        appearance.dark,
        appearance.contrast,
    )

    scss_colors_json_file = Dirs.CONFIG_DIR / "colors.json"
    scss_colors_json_file.write_text(
        json.dumps(colors, sort_keys=True, indent=2, separators=(",", ": "))
    )
    scss_colors_file = Dirs.CONFIG_DIR / "colors.scss"
    scss_colors_file.write_text(theme.scss)
    scss_palettes_file = Dirs.CONFIG_DIR / "palettes.scss"
    scss_palettes_file.write_text(preview)

    imports = [
        scss
        for scss in (Paths.path / "styles").glob("**/*.scss")
        if scss.name not in ("main.scss", "colors.scss", "palettes.scss")
    ]
    imports_text = "\n".join(f'@import "{scss}";' for scss in imports)

    main_scss_file = Dirs.CONFIG_DIR / "main.scss"
    main_scss_file.write_text(f"""@use \"{scss_colors_file}\" as c;
@use \"{scss_palettes_file}\" as p;

{imports_text}

* {{
  all: unset;
  font-family: JetBrainsMono;
  font-weight: bold;
  transition: all 0.2s ease;
}}""")
