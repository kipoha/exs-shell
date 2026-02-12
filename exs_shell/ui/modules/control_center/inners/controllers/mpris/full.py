import asyncio
from typing import Any, Callable

from ignis.widgets import Box, Button, CenterBox, Label, Overlay, Picture, Scale
from ignis.services.mpris import MprisPlayer

from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.widgets.custom.audio_visualizer import CircularAudioVisualizer
from exs_shell.ui.widgets.windows import Revealer
from exs_shell.utils.path import Paths


class Player(Box):
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
            css_classes=["control-center-player-title"],
        )
        self.artist_label = Label(
            label=player.bind("artist") if player else "N/A",
            ellipsize="end",
            max_width_chars=35,
            css_classes=["control-center-player-artist"],
        )

        self.picture = Picture(
            image=player.bind("art_url")
            if player
            else Paths.generate_path("icons/default/default.png", Paths.assets),
            content_fit="cover",
            width=80,
            height=80,
            css_classes=["control-center-mpris-art"],
        )
        self.cava = CircularAudioVisualizer(
            valign="center",
            halign="center",
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
            css_classes=["control-center-player-play"],
        )

        self.prev_button = Button(
            child=Label(label=Icons.player.PREVIOUS),
            on_click=(lambda _: asyncio.create_task(player.previous_async()))
            if player
            else None,
            css_classes=["control-center-player-prev"],
        )
        self.next_button = Button(
            child=Label(label=Icons.player.NEXT),
            on_click=(lambda _: asyncio.create_task(player.next_async()))
            if player
            else None,
            css_classes=["control-center-player-next"],
        )

        self.reveal_button = Button(
            child=Label(label=Icons.ui.DOWN),
            on_click=on_toggle,
            css_classes=["control-center-player-reveal"],
        )

        self.scale = Scale(
            value=player.bind("position") if player else 0,
            max=player.bind("length") if player else 1,
            hexpand=True,
            css_classes=["control-center-player-scale"],
            on_change=(
                lambda val: asyncio.create_task(player.set_position_async(val.value))
            )
            if player
            else None,
        )

        info_box = Box(
            vertical=True,
            spacing=2,
            child=[self.title_label, self.artist_label],
            css_classes=["control-center-player-info"],
            valign="center",
            halign="center",
            hexpand=True,
        )

        controls_box = Box(
            spacing=5,
            valign="center",
            halign="end",
            child=[self.prev_button, self.play_button, self.next_button],
            css_classes=["control-center-player-controller"],
            # hexpand=True,
        )

        control_info_box = CenterBox(
            valign="center",
            halign="center",
            start_widget=info_box,
            center_widget=controls_box,
            end_widget=self.reveal_button,
            css_classes=["control-center-player-controller-info"],
        )
        self.picture_box = Box(
            child=[self.picture],
            css_classes=["control-center-mpris-art-container"],
            halign="center",
            valign="center",
        )
        self.cava_overlay = Overlay(
            child=self.picture_box,
            overlays=[self.cava],
            css_classes=["control-center-mpris-art-overlay"],
        )
        self._inner = Box(
            vexpand=True,
            hexpand=True,
            vertical=True,
            halign="center",
            child=[
                self.cava_overlay,
                self.scale,
                control_info_box,
            ],
            css_classes=["control-center-player-background"],
        )

        self.revealer = Revealer(
            self._inner,
            RevealerTransition.SLIDE_UP,
            300,
            reveal_child=True,
        )

        super().__init__(
            spacing=10,
            valign="center",
            halign="center",
            css_classes=["control-center-player"],
            child=[self.revealer],
        )
