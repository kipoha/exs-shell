from exs_shell.utils.path import Dirs, Paths


def build_scss():
    scss_colors_file = Dirs.CONFIG_DIR / "colors.scss"
    scss_palettes_file = Dirs.CONFIG_DIR / "palettes.scss"
    main_scss_file = Dirs.CONFIG_DIR / "main.scss"

    scss_colors_file.touch()
    scss_palettes_file.touch()
    main_scss_file.touch()

    imports = [
        scss
        for scss in (Paths.path / "styles").glob("**/*.scss")
        if scss.name not in ("main.scss", "colors.scss", "palettes.scss")
    ]
    imports_text = "\n".join(f'@import "{scss}";' for scss in imports)

    main_scss_file.write_text(f"""@use \"{scss_colors_file}\" as c;
@use \"{scss_palettes_file}\" as p;

{imports_text}

* {{
  all: unset;
  font-family: JetBrainsMono;
  font-weight: bold;
  transition: all 0.2s ease;
}}""")
