import asyncio

from ignis import widgets
from ignis.services.mpris import MprisService, MprisPlayer

from modules.bar.childs.cava.widget import CavaManager
from modules.dashboard.widgets.cava import AudioVisualizer


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
                css_classes=["dashboard-widget-mpris-play"],
            )

            self.prev_button = widgets.Button(
                child=widgets.Icon(image="media-skip-backward-symbolic", pixel_size=18),
                on_click=lambda _: asyncio.create_task(player.previous_async()),
                css_classes=["dashboard-widget-mpris-prev"],
            )
            self.next_button = widgets.Button(
                child=widgets.Icon(image="media-skip-forward-symbolic", pixel_size=18),
                on_click=lambda _: asyncio.create_task(player.next_async()),
                css_classes=["dashboard-widget-mpris-next"],
            )

            self.scale = widgets.Scale(
                value=player.bind("position"),
                max=player.bind("length"),
                hexpand=True,
                css_classes=["dashboard-widget-mpris-scale"],
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
                css_classes=["dashboard-widget-mpris-play"],
            )
            self.prev_button = widgets.Button(
                child=widgets.Icon(image="media-skip-backward-symbolic", pixel_size=18),
                sensitive=False,
                css_classes=["dashboard-widget-mpris-prev"],
            )
            self.next_button = widgets.Button(
                child=widgets.Icon(image="media-skip-forward-symbolic", pixel_size=18),
                sensitive=False,
                css_classes=["dashboard-widget-mpris-next"],
            )
            self.scale = widgets.Scale(
                value=0,
                max=1,
                hexpand=True,
                sensitive=False,
                css_classes=["dashboard-widget-mpris-scale"],
            )

        if player and player.art_url:
            self.picture = widgets.Picture(
                image=player.bind("art_url"),
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
        else:
            self.picture = None
            container = None
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

    # def __init__(self, player: MprisPlayer):
    #     self._player = player
    #
    #     if player.art_url:
    #         pixbuf = load_pixbuf_from_url(player.art_url, 400, 200)
    #         self.bg = widgets.Picture(image=pixbuf)
    #     else:
    #         self.bg = widgets.Box()
    #     self.bg.hexpand = True
    #     self.bg.vexpand = True
    #
    #     self.visual = widgets.Box(spacing=2)
    #     self.visual.hexpand = True
    #     self.visual.vexpand = True
    #     self.bar_widgets = []
    #     for _ in range(20):
    #         bar = widgets.Box()
    #         bar.hexpand = True
    #         bar.vexpand = True
    #         self.visual.append(bar)
    #         self.bar_widgets.append(bar)
    #     cava.subscribe_values(self.update_visual)
    #
    #     self.icon = widgets.Icon(icon_name=self.get_player_icon(), pixel_size=24)
    #     self.icon.valign = "center"
    #
    #     self.title_label = widgets.Label(label=player.bind("title"), ellipsize="end")
    #     self.artist_label = widgets.Label(label=player.bind("artist"), ellipsize="end")
    #
    #     info_box = widgets.Box(vertical=True, spacing=2)
    #     info_box.append(self.title_label)
    #     info_box.append(self.artist_label)
    #     info_box.hexpand = True
    #
    #     self.play_button = widgets.Button(
    #         child=widgets.Icon(
    #             image=player.bind(
    #                 "playback_status",
    #                 lambda val: "media-playback-pause-symbolic"
    #                 if val == "Playing"
    #                 else "media-playback-start-symbolic",
    #             )
    #         )
    #     )
    #     self.prev_button = widgets.Button(
    #         child=widgets.Icon(image="media-skip-backward-symbolic")
    #     )
    #     self.next_button = widgets.Button(
    #         child=widgets.Icon(image="media-skip-forward-symbolic")
    #     )
    #
    #     controls_box = widgets.Box(spacing=5)
    #     controls_box.append(self.prev_button)
    #     controls_box.append(self.play_button)
    #     controls_box.append(self.next_button)
    #
    #     top_box = widgets.Box(spacing=8)
    #     top_box.append(self.icon)
    #     top_box.append(info_box)
    #     top_box.append(controls_box)
    #
    #     self.scale = widgets.Scale(
    #         value=player.bind("position"), max=player.bind("length")
    #     )
    #     self.scale.hexpand = True
    #
    #     content_box = widgets.Box(vertical=True, spacing=5)
    #     content_box.append(top_box)
    #     content_box.append(self.scale)
    #     content_box.append(self.visual)
    #     content_box.hexpand = True
    #     content_box.vexpand = True
    #
    #     super().__init__(child=self.bg, overlays=[content_box])
    #
    # def get_player_icon(self):
    #     entry = self._player.desktop_entry
    #     if entry in PLAYER_ICONS:
    #         return PLAYER_ICONS[entry]
    #     if self._player.track_id and "chrome" in self._player.track_id:
    #         return PLAYER_ICONS["chrome"]
    #     return PLAYER_ICONS[None]
    #
    # def update_visual(self, values):
    #     for bar, val in zip(self.bar_widgets, values):
    #         bar.set_size_request(-1, int(val * 100))
