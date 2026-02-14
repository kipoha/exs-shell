from typing import Any

from ignis.widgets import Box, Button, Label, Overlay
from ignis.services.power_profiles import PowerProfilesService

from exs_shell import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.state import State
from exs_shell.ui.widgets.windows import Revealer


@register.event
class PowerProfile(Box):
    def __init__(self, scale: float = 1.0, **kwargs):
        self.scale = scale
        self.power_profiles: PowerProfilesService = State.services.power_profiles

        active: str = self.power_profiles.active_profile  # type: ignore
        self.icon = Label(
            label=Icons.power_profiles.icon(active),
            css_classes=["control-center-system-power-profile-icon"],
        )
        self.label = Label(
            label=Icons.power_profiles.label(active),
            css_classes=["control-center-system-power-profile-label"],
        )
        self.button = Button(
            child=Box(
                css_classes=["control-center-system-power-profile-button"],
                child=[self.icon, self.label],
            ),
            on_click=self.toggle,
        )
        self.buttons = [
            Button(
                child=Box(
                    css_classes=[f"control-center-system-power-profile-select-{key}"],
                    child=[
                        Label(
                            label=icon_str,
                            css_classes=[
                                f"control-center-system-power-profile-select-icon-{key}"
                            ],
                        ),
                        Label(
                            label=label_str,
                            css_classes=[
                                f"control-center-system-power-profile-select-label-{key}"
                            ],
                        ),
                    ],
                    spacing=3 * self.scale,
                ),
                on_click=lambda _: self.select_profile(key),
            )
            for key, (icon_str, label_str) in Icons.power_profiles.raw.items()
        ]
        self.selects = Box(
            css_classes=["control-center-system-power-profile-selects"],
            vertical=True,
            child=self.buttons,
            vexpand=True,
        )
        self._revealer = Revealer(
            self.selects,
            RevealerTransition.SLIDE_DOWN,
            300,
            vexpand=True,
            hexpand=True,
            margin_top=20 * self.scale,
        )
        self._overlay = Overlay(
            child=self.button,
            overlays=[self._revealer],
            vexpand=True,
        )
        super().__init__(child=[self._overlay], **kwargs)

    @register.events.power_profiles("notify::active-profile")
    def __on_active_profile(self, service: PowerProfilesService, *_: Any):
        active: str = service.active_profile  # type: ignore
        self.icon.label = Icons.power_profiles.icon(active)
        self.label.label = Icons.power_profiles.label(active)

    def toggle(self, *_: Any):
        print("toggle", self._revealer.reveal_child)
        self._revealer.set_reveal_child(not self._revealer.reveal_child)

    def select_profile(self, key: str):
        self.power_profiles.set_active_profile(key)
        self._revealer.set_reveal_child(False)
