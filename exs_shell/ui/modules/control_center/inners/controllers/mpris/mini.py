import asyncio

from typing import Any, Callable

from ignis.widgets import Box, Button, CenterBox, Label, Overlay, Picture
from ignis.services.mpris import MprisPlayer

from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.widgets.custom.audio_visualizer import AudioVisualizer
from exs_shell.ui.widgets.windows import Revealer
from exs_shell.utils.path import Paths


class MiniPlayer(Box):
    def __init__(
        self,
        player: MprisPlayer | None = None,
        on_toggle: Callable[[Any], None] | None = None,
    ):
        self._player = player

        self.title_label = Label(
            label=player.bind("title") if player else "N/A",
            ellipsize="end",
            max_width_chars=35,
            css_classes=["control-center-mini-player-title"],
        )
        self.artist_label = Label(
            label=player.bind("artist") if player else "N/A",
            ellipsize="end",
            max_width_chars=35,
            css_classes=["control-center-mini-player-artist"],
        )

        self.picture = Picture(
            image=player.bind("art_url")
            if player
            else Paths.generate_path("icons/default/default.png", Paths.assets),
            content_fit="cover",
            width=400,
            height=50,
            css_classes=["control-center-mpris-art"],
        )
        self.cava = Box(
            valign="center",
            halign="center",
            child=[
                AudioVisualizer(
                    width=185,
                    css_classes=["control-center-audio-visualizer"],
                ),
                AudioVisualizer(
                    width=185,
                    css_classes=["control-center-audio-visualizer"],
                    mirror=True,
                ),
            ],
        )

        self.play_button = Button(
            child=Label(
                label=player.bind(
                    "playback_status",
                    lambda val: (
                        Icons.player.PAUSE if val == "Playing" else Icons.player.PLAY
                    ),
                )
                if player
                else "",
            ),
            on_click=(lambda _: asyncio.create_task(player.play_pause_async()))
            if player
            else None,
            css_classes=["control-center-mini-player-play"],
        )

        self.prev_button = Button(
            child=Label(label=Icons.player.PREVIOUS),
            on_click=(lambda _: asyncio.create_task(player.previous_async()))
            if player
            else None,
            css_classes=["control-center-mini-player-prev"],
        )
        self.next_button = Button(
            child=Label(label=Icons.player.NEXT),
            on_click=(lambda _: asyncio.create_task(player.next_async()))
            if player
            else None,
            css_classes=["control-center-mini-player-next"],
        )

        self.reveal_button = Button(
            child=Label(label=Icons.ui.UP),
            on_click=on_toggle,
            css_classes=["control-center-mini-player-reveal"],
        )

        info_box = Box(
            vertical=True,
            spacing=2,
            child=[self.title_label, self.artist_label],
            css_classes=["control-center-mini-player-info"],
            valign="center",
            halign="center",
            hexpand=True,
        )

        controls_box = Box(
            spacing=5,
            valign="center",
            halign="end",
            child=[self.prev_button, self.play_button, self.next_button],
            css_classes=["control-center-mini-player-controller"],
        )

        control_info_box = CenterBox(
            valign="center",
            halign="center",
            start_widget=info_box,
            center_widget=controls_box,
            end_widget=self.reveal_button,
            css_classes=["control-center-mini-player-controller-info"],
        )
        self.back_overlay = Overlay(child=self.picture, overlays=[self.cava])
        self.background = Overlay(
            child=self.back_overlay,
            overlays=[
                Box(
                    vexpand=True,
                    hexpand=True,
                    css_classes=["control-center-mini-player-background"],
                )
            ],
        )
        self.overlay = Overlay(child=self.background, overlays=[control_info_box])

        self.revealer = Revealer(
            self.overlay,
            RevealerTransition.SLIDE_DOWN,
            300,
            reveal_child=True,
        )

        super().__init__(
            spacing=10,
            valign="center",
            halign="center",
            css_classes=["control-center-mini-player"],
            child=[self.revealer],
        )
