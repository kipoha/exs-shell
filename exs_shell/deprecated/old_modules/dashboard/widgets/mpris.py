import asyncio

from ignis import widgets
from ignis.services.mpris import MprisService, MprisPlayer

from exs_shell.utils.path import PathUtils
from exs_shell.modules.bar.childs.cava.widget import CavaManager
from exs_shell.modules.dashboard.widgets.cava import AudioVisualizer


mpris = MprisService.get_default()
cava = CavaManager.get_default()

PLAYER_ICONS = {
    "spotify": "spotify-symbolic",
    "firefox": "firefox-symbolic",
    "chrome": "chrome-symbolic",
    None: "folder-music-symbolic",
}


class MprisPlayerWidget(widgets.Box):
    def __init__(self, player: MprisPlayer | None = None):
        self._player = player

        self.icon = widgets.Icon(
            icon_name=self.get_player_icon(),
            pixel_size=24,
            css_classes=["dashboard-widget-mpris-icon"],
        )

        self.title_label = widgets.Label(
            label=player.bind("title") if player else "N/A",
            ellipsize="end",
            max_width_chars=20,
            css_classes=["dashboard-widget-mpris-title"],
        )
        self.artist_label = widgets.Label(
            label=player.bind("artist") if player else "N/A",
            ellipsize="end",
            max_width_chars=20,
            css_classes=["dashboard-widget-mpris-artist"],
        )

        self.play_button = widgets.Button(
            child=widgets.Icon(
                image=player.bind(
                    "playback_status",
                    lambda val: "media-playback-pause-symbolic"
                    if val == "Playing"
                    else "media-playback-start-symbolic",
                )
                if player
                else "media-playback-start-symbolic",
                pixel_size=18,
            ),
            on_click=(lambda _: asyncio.create_task(player.play_pause_async()))
            if player
            else None,
            css_classes=["dashboard-widget-mpris-play"],
        )

        self.prev_button = widgets.Button(
            child=widgets.Icon(image="media-skip-backward-symbolic", pixel_size=18),
            on_click=(lambda _: asyncio.create_task(player.previous_async()))
            if player
            else None,
            css_classes=["dashboard-widget-mpris-prev"],
        )
        self.next_button = widgets.Button(
            child=widgets.Icon(image="media-skip-forward-symbolic", pixel_size=18),
            on_click=(lambda _: asyncio.create_task(player.next_async()))
            if player
            else None,
            css_classes=["dashboard-widget-mpris-next"],
        )

        self.scale = widgets.Scale(
            value=player.bind("position") if player else 0,
            max=player.bind("length") if player else 1,
            hexpand=True,
            css_classes=["dashboard-widget-mpris-scale"],
            on_change=(
                lambda val: asyncio.create_task(player.set_position_async(val.value))
                if player
                else None
            ),
        )

        self.picture = widgets.Picture(
            image=player.bind("art_url")
            if player
            else PathUtils.generate_path(
                "icons/default/default.png", PathUtils.assets_path
            ),
            content_fit="cover",
            width=100,
            height=100,
            css_classes=["dashboard-widget-mpris-art"],
        )

        container = widgets.CenterBox(
            start_widget=AudioVisualizer(),
            center_widget=self.picture,
            end_widget=AudioVisualizer(mirror=True),
        )
        info_box = widgets.Box(
            vertical=True,
            spacing=2,
            child=[self.title_label, self.artist_label],
            css_classes=["dashboard-widget-mpris-info"],
        )

        controls_box = widgets.Box(
            spacing=5,
            valign="center",
            halign="center",
            child=[self.prev_button, self.play_button, self.next_button],
            css_classes=["dashboard-widget-mpris-controls"],
        )

        super().__init__(
            spacing=10,
            vertical=True,
            valign="center",
            halign="center",
            css_classes=["dashboard-widget-mpris"],
            child=[self.icon, container, info_box, controls_box, self.scale],
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
