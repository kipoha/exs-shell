from typing import Any

from ignis.widgets import Box, Button
from ignis.services.power_profiles import PowerProfilesService

from exs_shell import register
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.state import State
from exs_shell.ui.widgets.custom.icon import Icon


@register.event
class PowerProfile(Box):
    def __init__(self, scale: float = 1.0, **kwargs):
        self.scale = scale
        self.power_profiles: PowerProfilesService = State.services.power_profiles
        active: str = self.power_profiles.active_profile  # type: ignore

        self.buttons = [
            Button(
                child=Box(
                    css_classes=[
                        f"control-center-quick-panel-power-profile-select-{key}-box"
                    ],
                    child=[
                        Icon(
                            label=icon_str,
                            size="m",
                        )
                    ],
                    spacing=3 * self.scale,
                    hexpand=True,
                ),
                css_classes=[
                    f"control-center-quick-panel-power-profile-select-{key}-button",
                    "active" if key == active else "",
                ],
                on_click=lambda _, k=key: self.power_profiles.set_active_profile(k),
                halign="fill",
            )
            for key, (icon_str, _) in Icons.power_profiles.raw.items()
        ]
        self.selects = Box(
            css_classes=["control-center-quick-panel-power-profile-selects"],
            child=self.buttons,
            spacing=5 * self.scale,
            hexpand=True,
        )
        super().__init__(
            child=[self.selects],
            hexpand=True,
            css_classes=["control-center-quick-panel-power-profile"],
            **kwargs,
        )

    @register.events.power_profiles("notify::active-profile")
    def __on_active_profile(self, service: PowerProfilesService, *_: Any):
        active: str = service.active_profile  # type: ignore
        for b in self.buttons:
            b.remove_css_class("active")
            for css in b.css_classes:
                if active in css:
                    b.add_css_class("active")
