from typing import Type

from ignis import widgets
from ignis.services.mpris import MprisPlayer, MprisService


mpris = MprisService.get_default()


class Player:
    def __init__(self, player: MprisPlayer | None = None):
        raise NotImplementedError


class MprisPlayerManager(widgets.Box):
    def __init__(self, mpris_cls: Type[Player], css_name: str):
        self.mpris_cls = mpris_cls
        super().__init__(
            vertical=True,
            spacing=5,
            css_classes=[f"dashboard-widget-{css_name}-manager"],
        )

        self._placeholder = self.mpris_cls(None)
        self._players_map: dict[MprisPlayer, Player] = {}

        for player in mpris.get_players():
            self._add_player_internal(player)

        if not self._players_map:
            self.append(self._placeholder)

        mpris.connect("player_added", lambda _, player: self._on_player_added(player))

    def _on_player_added(self, player: MprisPlayer):
        if self._placeholder in self:
            self.remove(self._placeholder)
        self._add_player_internal(player)

    def _add_player_internal(self, player: MprisPlayer):
        mp = self.mpris_cls(player)
        self.append(mp)
        self._players_map[player] = mp

        def _on_player_closed(p):
            self._remove_player_internal(player)

        try:
            player.connect("closed", lambda p: _on_player_closed(p))
        except Exception:
            pass

    def _remove_player_internal(self, player: MprisPlayer):
        widget = self._players_map.pop(player, None)
        if widget and widget in self:
            self.remove(widget)

        if not self._players_map and self._placeholder not in self:
            self.append(self._placeholder)
