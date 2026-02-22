from ignis.options_manager import OptionsGroup


class Weather(OptionsGroup):
    location: str = "New-York"
    farenheit: bool = False
