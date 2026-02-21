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
}}

.icon {{
  font-family: "Material Symbols Rounded", "Material Icons Rounded";

  &.xs {{
    font-size: 0.8rem;
  }}

  &.s {{
    font-size: 1rem;
  }}

  &.m {{
    font-size: 1.5rem;
  }}

  &.l {{
    font-size: 2rem;
  }}

  &.xl {{
    font-size: 2.5rem;
  }}

  &.xxl {{
    font-size: 3rem;
  }}

  &.xxxl {{
    font-size: 3.5rem;
  }}
}}

entry {{
    background-color: c.$surface_container_low;
    color: c.$on_surface;
}}

entry selection {{
    background-color: c.$primary;
    color: c.$background;
}}""")
