import asyncio
from ignis import widgets
from ignis.services.mpris import MprisPlayer
from exs_shell.modules.dashboard.widgets.shared.mpris import Player

PLAYER_ICONS = {
    "spotify": "spotify-symbolic",
    "firefox": "firefox-symbolic",
    "chrome": "chrome-symbolic",
    None: "folder-music-symbolic",
}


class MiniPlayer(widgets.Box, Player):
    def __init__(self, player: MprisPlayer | None = None):
        self._player = player

        self.icon = widgets.Icon(
            icon_name=self.get_player_icon(),
            pixel_size=24,
            css_classes=["dashboard-widget-mini-player-icon"],
        )

        self.title_label = widgets.Label(
            label=player.bind("title") if player else "N/A",
            ellipsize="end",
            max_width_chars=20,
            css_classes=["dashboard-widget-mini-player-title"],
        )
        self.artist_label = widgets.Label(
            label=player.bind("artist") if player else "N/A",
            ellipsize="end",
            max_width_chars=20,
            css_classes=["dashboard-widget-mini-player-artist"],
        )

        if player:
            self.play_button = widgets.Button(
                child=widgets.Icon(
                    image=player.bind(
                        "playback_status",
                        lambda val: "media-playback-pause-symbolic"
                        if val == "Playing"
                        else "media-playback-start-symbolic",
                    ),
                    pixel_size=18,
                ),
                on_click=lambda _: asyncio.create_task(player.play_pause_async()),
                css_classes=["dashboard-widget-mini-player-play"],
            )

            self.prev_button = widgets.Button(
                child=widgets.Icon(image="media-skip-backward-symbolic", pixel_size=18),
                on_click=lambda _: asyncio.create_task(player.previous_async()),
                css_classes=["dashboard-widget-mini-player-prev"],
            )
            self.next_button = widgets.Button(
                child=widgets.Icon(image="media-skip-forward-symbolic", pixel_size=18),
                on_click=lambda _: asyncio.create_task(player.next_async()),
                css_classes=["dashboard-widget-mini-player-next"],
            )

            self.scale = widgets.Scale(
                value=player.bind("position"),
                max=player.bind("length"),
                hexpand=True,
                css_classes=["dashboard-widget-mini-player-scale"],
                on_change=lambda val: asyncio.create_task(
                    player.set_position_async(val.value)
                ),
                visible=player.bind("position", lambda v: v != -1),
            )
        else:
            self.play_button = widgets.Button(
                child=widgets.Icon(
                    image="media-playback-start-symbolic", pixel_size=18
                ),
                sensitive=False,
                css_classes=["dashboard-widget-mini-player-play"],
            )
            self.prev_button = widgets.Button(
                child=widgets.Icon(image="media-skip-backward-symbolic", pixel_size=18),
                sensitive=False,
                css_classes=["dashboard-widget-mini-player-prev"],
            )
            self.next_button = widgets.Button(
                child=widgets.Icon(image="media-skip-forward-symbolic", pixel_size=18),
                sensitive=False,
                css_classes=["dashboard-widget-mini-player-next"],
            )
            self.scale = widgets.Scale(
                value=0,
                max=1,
                hexpand=True,
                sensitive=False,
                css_classes=["dashboard-widget-mini-player-scale"],
            )

        info_box = widgets.Box(
            vertical=True,
            spacing=2,
            child=[self.title_label, self.artist_label],
            css_classes=["dashboard-widget-mini-player-info"],
        )

        controls_box = widgets.Box(
            spacing=5,
            valign="center",
            halign="center",
            child=[self.prev_button, self.play_button, self.next_button],
            css_classes=["dashboard-widget-mini-player-controls"],
        )

        super().__init__(
            spacing=10,
            vertical=True,
            valign="center",
            css_classes=["dashboard-widget-mini-player"],
            child=[self.icon, info_box, controls_box, self.scale],
        )

    def get_player_icon(self):
        if not self._player:
            return PLAYER_ICONS[None]
        entry = self._player.desktop_entry
        if entry in PLAYER_ICONS:
            return PLAYER_ICONS[entry]
        if self._player.track_id and "chrome" in self._player.track_id:
            return PLAYER_ICONS["chrome"]
        if self._player.track_id and "firefox" in self._player.track_id:
            return PLAYER_ICONS["firefox"]


# class MiniPlayerManager(widgets.Box):
#     def __init__(self):
#         super().__init__(
#             vertical=True,
#             spacing=5,
#             css_classes=["dashboard-widget-mini-player-manager"],
#         )
#
#         self._placeholder = MiniPlayer(None)
#         self._players_map: dict[MprisPlayer, MiniPlayer] = {}
#
#         for player in mpris.get_players():
#             self._add_player_internal(player)
#
#         if not self._players_map:
#             self.append(self._placeholder)
#
#         mpris.connect("player_added", lambda _, player: self._on_player_added(player))
#
#     def _on_player_added(self, player: MprisPlayer):
#         if self._placeholder in self:
#             self.remove(self._placeholder)
#         self._add_player_internal(player)
#
#     def _add_player_internal(self, player: MprisPlayer):
#         mp = MiniPlayer(player)
#         self.append(mp)
#         self._players_map[player] = mp
#
#         def _on_player_closed(p):
#             self._remove_player_internal(player)
#
#         try:
#             player.connect("closed", lambda p: _on_player_closed(p))
#         except Exception:
#             pass
#
#     def _remove_player_internal(self, player: MprisPlayer):
#         widget = self._players_map.pop(player, None)
#         if widget and widget in self:
#             self.remove(widget)
#
#         if not self._players_map and self._placeholder not in self:
#             self.append(self._placeholder)
