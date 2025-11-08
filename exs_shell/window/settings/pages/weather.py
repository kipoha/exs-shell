from ..elements import (
    SwitchRow,
    EntryRow,
    SettingsPage,
    SettingsGroup,
    SettingsEntry,
)
from exs_shell.config.user import options


class WeatherEntry(SettingsEntry):
    def __init__(self):
        page = SettingsPage(
            name="Weather",
            groups=[
                SettingsGroup(
                    name="General",
                    rows=[
                        EntryRow(
                            label="Location",
                            text=options.weather.bind("location"),
                            on_change=lambda value: options.weather.set_location(
                                value.text
                            ),
                            # width=200,
                        ),
                        SwitchRow(
                            label="Farenheit",
                            active=options.weather.bind("farenheit"),
                            on_change=lambda x, state: options.weather.set_farenheit(
                                state
                            ),
                        ),
                    ],
                )
            ],
        )
        super().__init__(
            label="Weather",
            icon="󰖐",
            page=page,
        )
