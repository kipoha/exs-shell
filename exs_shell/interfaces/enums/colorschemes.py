from enum import Enum, StrEnum

from materialyoucolor.scheme.variant import Variant
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
from materialyoucolor.scheme.scheme_vibrant import SchemeVibrant
from materialyoucolor.scheme.scheme_content import SchemeContent
from materialyoucolor.scheme.scheme_neutral import SchemeNeutral
from materialyoucolor.scheme.scheme_rainbow import SchemeRainbow
from materialyoucolor.scheme.scheme_fidelity import SchemeFidelity
from materialyoucolor.scheme.scheme_fruit_salad import SchemeFruitSalad
from materialyoucolor.scheme.scheme_monochrome import SchemeMonochrome
from materialyoucolor.scheme.scheme_expressive import SchemeExpressive

from exs_shell.interfaces.protocols.colorscheme import ColorSchemeInterface


class ColorSchemes(StrEnum):
    MONOCHROME = Variant.MONOCHROME
    TONAL_SPOT = Variant.TONAL_SPOT
    VIBRANT = Variant.VIBRANT
    EXPRESSIVE = Variant.EXPRESSIVE
    FIDELITY = Variant.FIDELITY
    CONTENT = Variant.CONTENT
    RAINBOW = Variant.RAINBOW
    FRUIT_SALAD = Variant.FRUIT_SALAD
    NEUTRAL = "NEUTRAL"


class ColorSchemeClasses(Enum):
    MONOCHROME = SchemeMonochrome
    TONAL_SPOT = SchemeTonalSpot
    VIBRANT = SchemeVibrant
    EXPRESSIVE = SchemeExpressive
    FIDELITY = SchemeFidelity
    CONTENT = SchemeContent
    RAINBOW = SchemeRainbow
    FRUIT_SALAD = SchemeFruitSalad
    NEUTRAL = SchemeNeutral
    
    @classmethod
    def get(cls, enum: ColorSchemes | str) -> ColorSchemeInterface:
        return cls[enum].value  # type: ignore


class ColorSchemes2(StrEnum):
    CONTENT = "content"
    EXPRESSIVE = "expressive"
    FIDELITY = "fidelity"
    FRUIT_SALAD = "fruit-salad"
    MONOCHROME = "monochrome"
    NEUTRAL = "neutral"
    RAINBOW = "rainbow"
    TONAL_SPOT = "tonal-spot"
