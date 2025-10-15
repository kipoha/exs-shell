from ignis import widgets
from window.settings.elements import (
    SettingsPage,
    SettingsGroup,
    SettingsEntry,
    SwitchRow,
    SpinRow,
    FileRow,
    EntryRow,
    SelectRow,
    MultiSelectRow,
    SliderRow,
)


class TestEntry(SettingsEntry):
    def __init__(self):
        page = SettingsPage(
            name="Bar",
            groups=[
                SettingsGroup(
                    name="General",
                    rows=[
                        SwitchRow(
                            label="Switch",
                            sublabel="Switch description",
                            on_change=lambda x, state: print(x, state),
                        ),
                        SpinRow(
                            label="Spin",
                            sublabel="Spin description",
                            value=1000,
                            min=1,
                            on_change=lambda x, value: print(x, value),
                        ),
                        SelectRow(
                            label="Select",
                            options=["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"],
                            on_selected=lambda x: print(x),
                        ),
                        EntryRow(
                            label="Entry",
                            sublabel="Entry description",
                            width=200,
                            on_change=lambda value: print(value),
                        ),
                        FileRow(
                            label="File",
                            dialog=widgets.FileDialog(),
                            sublabel="File description",
                            button_label="Change",
                        ),
                        SliderRow(
                            label="Slider",
                            min=0,
                            max=100,
                            value=50,
                            on_change=lambda value: print(value),
                        ),
                        MultiSelectRow(
                            label="Multi select",
                            options=["Option 1", "Option 2", "Option 3"],
                            on_change=lambda x: print(x),
                        ),
                    ],
                )
            ],
        )
        super().__init__(
            label="Test",
            icon="test-symbolic",
            page=page,
        )
