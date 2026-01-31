from ..elements import (
    SettingsPage,
    SettingsGroup,
    SettingsEntry,
    SettingsRow
)


class BluetoothEntry(SettingsEntry):
    def __init__(self):
        page = SettingsPage(
            name="Bluetooth",
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
            label="Bluetooth",
            icon="",
            page=page,
        )
