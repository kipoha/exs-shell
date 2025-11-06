import asyncio
from ignis import widgets
from ignis.services.mpris import MprisService, MprisPlayer
from modules.bar.childs.cava.widget import CavaManager

from gi.repository import GdkPixbuf  # type: ignore

mpris = MprisService.get_default()
cava = CavaManager.get_default()

PLAYER_ICONS = {
    "spotify": "spotify-symbolic",
    "firefox": "firefox-browser-symbolic",
    "chrome": "chrome-symbolic",
    None: "folder-music-symbolic",
}


def load_pixbuf_from_url(url, width, height):
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(url)
    pixbuf = pixbuf.scale_simple(400, 200, GdkPixbuf.InterpType.BILINEAR)
    if width and height:
        pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
    return pixbuf


class MprisPlayerWidget(widgets.Overlay):
    def __init__(self, player: MprisPlayer):
        self._player = player

        if player.art_url:
            pixbuf = load_pixbuf_from_url(player.art_url, 400, 200)
            self.bg = widgets.Picture(image=pixbuf)
        else:
            self.bg = widgets.Box()
        self.bg.hexpand = True
        self.bg.vexpand = True

        # ===== Визуализатор =====
        self.visual = widgets.Box(spacing=2)
        self.visual.hexpand = True
        self.visual.vexpand = True
        self.bar_widgets = []
        for _ in range(20):
            bar = widgets.Box()
            bar.hexpand = True
            bar.vexpand = True
            self.visual.append(bar)
            self.bar_widgets.append(bar)
        cava.subscribe_values(self.update_visual)

        self.icon = widgets.Icon(icon_name=self.get_player_icon(), pixel_size=24)
        self.icon.valign = "center"

        self.title_label = widgets.Label(label=player.bind("title"), ellipsize="end")
        self.artist_label = widgets.Label(label=player.bind("artist"), ellipsize="end")

        info_box = widgets.Box(vertical=True, spacing=2)
        info_box.append(self.title_label)
        info_box.append(self.artist_label)
        info_box.hexpand = True

        self.play_button = widgets.Button(
            child=widgets.Icon(
                image=player.bind(
                    "playback_status",
                    lambda val: "media-playback-pause-symbolic"
                    if val == "Playing"
                    else "media-playback-start-symbolic",
                )
            )
        )
        self.prev_button = widgets.Button(
            child=widgets.Icon(image="media-skip-backward-symbolic")
        )
        self.next_button = widgets.Button(
            child=widgets.Icon(image="media-skip-forward-symbolic")
        )

        controls_box = widgets.Box(spacing=5)
        controls_box.append(self.prev_button)
        controls_box.append(self.play_button)
        controls_box.append(self.next_button)

        top_box = widgets.Box(spacing=8)
        top_box.append(self.icon)
        top_box.append(info_box)
        top_box.append(controls_box)

        self.scale = widgets.Scale(
            value=player.bind("position"), max=player.bind("length")
        )
        self.scale.hexpand = True

        content_box = widgets.Box(vertical=True, spacing=5)
        content_box.append(top_box)
        content_box.append(self.scale)
        content_box.append(self.visual)
        content_box.hexpand = True
        content_box.vexpand = True

        super().__init__(child=self.bg, overlays=[content_box])

    def get_player_icon(self):
        entry = self._player.desktop_entry
        if entry in PLAYER_ICONS:
            return PLAYER_ICONS[entry]
        if self._player.track_id and "chrome" in self._player.track_id:
            return PLAYER_ICONS["chrome"]
        return PLAYER_ICONS[None]

    def update_visual(self, values):
        for bar, val in zip(self.bar_widgets, values):
            bar.set_size_request(-1, int(val * 100))


class MprisPlayerManager(widgets.Box):

    def __init__(self):
        super().__init__(
            vertical=True, spacing=5, css_classes=["dashboard-widget-mpris-manager"]
        )
        mpris.connect("player_added", lambda _, player: self.add_player(player))

    def add_player(self, player: MprisPlayer):
        widget = MprisPlayerWidget(player)
        self.append(widget)
