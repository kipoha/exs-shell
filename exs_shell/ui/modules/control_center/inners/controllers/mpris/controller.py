from ignis.widgets import Box
from ignis.services.mpris import MprisPlayer, MprisService

from exs_shell import register
from exs_shell.state import State
from exs_shell.ui.modules.control_center.inners.controllers.mpris.full import Player
from exs_shell.ui.modules.control_center.inners.controllers.mpris.mini import MiniPlayer


@register.event
class MprisController(Box):
    def __init__(self):
        self.mpris: MprisService = State.services.mpris
        super().__init__(css_classes=["control-center-mpris"])

        self._players_map: dict[
            MprisPlayer, tuple[MiniPlayer, Player]
        ] = {}

        for player in self.mpris.players:
            self._add_player_internal(player)

    @register.events.mpris("player-added")
    def _on_player_added(self, _: MprisService, player: MprisPlayer):
        self._add_player_internal(player)

    def _add_player_internal(self, player: MprisPlayer):
        def toggle(_=None):
            mini, full = self._players_map[player]

            mini.revealer.reveal_child = not mini.revealer.reveal_child
            full.revealer.reveal_child = not full.revealer.reveal_child

       
        mini = MiniPlayer(player, on_toggle=toggle)
        full = Player(player, on_toggle=toggle)

        full.revealer.reveal_child = False

        container = Box(
            vertical=True,
            child=[full, mini],
        )

        self.append(container)
        self._players_map[player] = (mini, full)

        try:
            player.connect("closed", lambda _: self._remove_player_internal(player))
        except Exception:
            pass

    def _remove_player_internal(self, player: MprisPlayer):
        pair = self._players_map.pop(player, None)
        if not pair:
            return

        mini, full = pair
        parent = mini.get_parent()
        if parent:
            self.remove(parent)
