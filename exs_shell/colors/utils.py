# type: ignore
from PIL import Image

from materialyoucolor.scheme import Scheme
# from materialyoucolor.utils.color_utils import argb_from_rgba
# from materialyoucolor.palettes.core_palette import CorePalette

from exs_shell.config.user import options

def generate_theme(wallpaper_path: str | None = options.wallpaper.wallpaper_path) -> tuple[dict | None, str | None]:
    scss_text = None
    theme_json = None
    if wallpaper_path:
        img = Image.open(wallpaper_path).convert("RGB")
        pixels = list(img.getdata())

        r = sum(p[0] for p in pixels) // len(pixels)
        g = sum(p[1] for p in pixels) // len(pixels)
        b = sum(p[2] for p in pixels) // len(pixels)
        seed_rgb = [r, g, b, 255]

        scheme = Scheme.dark_from_rgb(seed_rgb)

        def to_scss_color(val) -> str:
            if isinstance(val, int):
                a = (val >> 24) & 0xFF
                r = (val >> 16) & 0xFF
                g = (val >> 8) & 0xFF
                b = val & 0xFF
                if a == 255:
                    return f"#{r:02X}{g:02X}{b:02X}"
                else:
                    return f"rgba({r},{g},{b},{a/255:.2f})"

            if isinstance(val, (list, tuple)) and len(val) in (3, 4):
                r, g, b = val[:3]
                a = val[3] if len(val) == 4 else 255
                if a == 255:
                    return f"#{r:02X}{g:02X}{b:02X}"
                else:
                    return f"rgba({r},{g},{b},{a/255:.2f})"

            if isinstance(val, str):
                return val

            raise ValueError(f"Cannot convert {val} to SCSS color")

        theme_json = {
            "bg": to_scss_color(scheme.background),
            "bg-light": to_scss_color(scheme.surfaceVariant),
            "fg": to_scss_color(scheme.onSurface),
            "active": to_scss_color(scheme.primary),
            "unactive": to_scss_color(scheme.secondary),
            "bg-dark": to_scss_color(scheme.surface),
            "bg-darker": to_scss_color(scheme.background),
            "bg-lighter": to_scss_color(scheme.surfaceVariant),
            "surface": to_scss_color(scheme.surface),
            "surface-light": to_scss_color(scheme.surfaceVariant),
            "fg-strong": "#ffffff",
            "fg-muted": to_scss_color(scheme.onSurfaceVariant),
            "fg-disabled": to_scss_color(scheme.onSurfaceVariant),
            "accent": to_scss_color(scheme.primary),
            "accent-light": to_scss_color(scheme.primaryContainer),
            "accent-dark": to_scss_color(scheme.primary),
            "accent-muted": to_scss_color(scheme.secondary),
            "border": to_scss_color(scheme.outline),
            "border-light": to_scss_color(scheme.outlineVariant),
            "shadow": "rgba(0, 0, 0, 0.4)",
            "success": "#a3f7b5",
            "warning": "#f7e3a3",
            "error": "#f28b82",
            "info": "#a3d9f7"
        }

        scss_text = "\n".join([f"${k}: {to_scss_color(v)};" for k, v in theme_json.items()])

    return theme_json, scss_text
