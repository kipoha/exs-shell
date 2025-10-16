from window.settings.elements import (
    SettingsPage,
    SettingsGroup,
    SettingsEntry,
    MultiSelectRow,
    SpinRow
)
from modules.bar.childs import modules
from config.user import options


class BarEntry(SettingsEntry):
    def __init__(self):
        page = SettingsPage(
            name="Bar",
            groups=[
                SettingsGroup(
                    name="General",
                    rows=[
                        MultiSelectRow(
                            label="Left bar modules",
                            sublabel="Modules that will be displayed on the left of the bar",
                            options=modules.keys(),
                            selected_items=options.bar.left,
                            on_change=lambda value: options.bar.set_left(value),
                        ),
                        SpinRow(
                            label="Bar left spacing",
                            sublabel="Spacing between modules",
                            value=options.bar.bind("left_spacing"),
                            min=1,
                            max=100,
                            on_change=lambda x, value: options.bar.set_left_spacing(value),
                        ),
                        MultiSelectRow(
                            label="Center bar modules",
                            sublabel="Modules that will be displayed on the center of the bar",
                            options=modules.keys(),
                            selected_items=options.bar.center,
                            on_change=lambda value: options.bar.set_center(value),
                        ),
                        SpinRow(
                            label="Bar center spacing",
                            sublabel="Spacing between modules",
                            value=options.bar.bind("center_spacing"),
                            min=1,
                            max=100,
                            on_change=lambda x, value: options.bar.set_center_spacing(value),
                        ),
                        MultiSelectRow(
                            label="Right bar modules",
                            sublabel="Modules that will be displayed on the right of the bar",
                            options=modules.keys(),
                            selected_items=options.bar.right,
                            on_change=lambda value: options.bar.set_right(value),
                        ),
                        SpinRow(
                            label="Bar right spacing",
                            sublabel="Spacing between modules",
                            value=options.bar.bind("right_spacing"),
                            min=1,
                            max=100,
                            on_change=lambda x, value: options.bar.set_right_spacing(value),
                        ),
                    ],
                )
            ],
        )
        super().__init__(
            label="Bar",
            icon="",
            page=page,
        )
