from ..elements import (
    SettingsPage,
    SettingsGroup,
    SettingsEntry,
    SettingsRow
)


class WifiEntry(SettingsEntry):
    def __init__(self):
        page = SettingsPage(
            name="Wi-Fi",
            groups=[
                SettingsGroup(
                    name="General",
                    rows=[
                        SettingsRow(
                            label="Soon...",
                        )
                    ],
                )
            ],
        )
        super().__init__(
            label="Wi-Fi",
            icon="",
            page=page,
        )
