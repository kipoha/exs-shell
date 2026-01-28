from dataclasses import dataclass

@dataclass
class ThemeColors:
    bg: str
    bg_light: str
    fg: str
    active: str
    unactive: str
    bg_dark: str
    bg_darker: str
    bg_lighter: str
    surface: str
    surface_light: str
    fg_strong: str
    fg_muted: str
    fg_disabled: str
    accent: str
    accent_light: str
    accent_dark: str
    accent_muted: str
    border: str
    border_light: str
    shadow: str
    success: str = "#a1d6f1"
    warning: str = "#f9e2af"
    error: str = "#f38ba8"
    info: str = "#91d7f3"
