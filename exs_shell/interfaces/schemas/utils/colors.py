from dataclasses import dataclass, fields, asdict
from typing import Any, Callable, Self

from materialyoucolor.scheme.dynamic_scheme import DynamicScheme
from materialyoucolor.dynamiccolor.material_dynamic_colors import (
    MaterialDynamicColors as c,
)

from exs_shell.interfaces.enums.colorschemes import ColorSchemes
from exs_shell.interfaces.types import RGB


@dataclass(slots=True)
class MaterialColors:
    background: str
    onBackground: str

    surface: str
    surfaceDim: str
    surfaceBright: str
    surfaceContainerLowest: str
    surfaceContainerLow: str
    surfaceContainer: str
    surfaceContainerHigh: str
    surfaceContainerHighest: str

    onSurface: str
    surfaceVariant: str
    onSurfaceVariant: str

    inverseSurface: str
    inverseOnSurface: str

    outline: str
    outlineVariant: str

    shadow: str
    scrim: str
    surfaceTint: str

    primary: str
    onPrimary: str
    primaryContainer: str
    onPrimaryContainer: str
    inversePrimary: str

    secondary: str
    onSecondary: str
    secondaryContainer: str
    onSecondaryContainer: str

    tertiary: str
    onTertiary: str
    tertiaryContainer: str
    onTertiaryContainer: str

    error: str
    onError: str
    errorContainer: str
    onErrorContainer: str

    primaryFixed: str
    primaryFixedDim: str
    onPrimaryFixed: str
    onPrimaryFixedVariant: str

    secondaryFixed: str
    secondaryFixedDim: str
    onSecondaryFixed: str
    onSecondaryFixedVariant: str

    tertiaryFixed: str
    tertiaryFixedDim: str
    onTertiaryFixed: str
    onTertiaryFixedVariant: str

    @classmethod
    def create(cls, scheme: DynamicScheme, converter: Callable[[Any], str]) -> Self:
        return cls(
            **{
                field.name: cls._get_color(scheme, converter, field.name)
                for field in fields(cls)
            }
        )

    @classmethod
    def _get_color(
        cls, scheme: DynamicScheme, converter: Callable[[Any], str], color: str
    ) -> str:
        return converter(getattr(c, color).get_argb(scheme))


@dataclass(slots=True)
class GeneratedTheme:
    colors: MaterialColors
    scss: str
    scheme: ColorSchemes
    seed_rgb: RGB


@dataclass(slots=True)
class GeneratedPreviewColors:
    primary: str
    secondary: str
    tertiary: str

    @classmethod
    def create(cls, scheme: DynamicScheme, converter: Callable[[Any], str]) -> Self:
        return cls(
            **{
                field.name: cls._get_color(scheme, converter, field.name)
                for field in fields(cls)
            }
        )

    @classmethod
    def _get_color(
        cls, scheme: DynamicScheme, converter: Callable[[Any], str], color: str
    ) -> str:
        return converter(getattr(c, color).get_argb(scheme))


@dataclass(slots=True)
class ColorSchemeList:
    monochrome: GeneratedPreviewColors
    tonal_spot: GeneratedPreviewColors
    vibrant: GeneratedPreviewColors
    expressive: GeneratedPreviewColors
    fidelity: GeneratedPreviewColors
    content: GeneratedPreviewColors
    rainbow: GeneratedPreviewColors
    fruit_salad: GeneratedPreviewColors
    neutral: GeneratedPreviewColors

    def asdict(self) -> dict[str, Any]:
        return asdict(self)
