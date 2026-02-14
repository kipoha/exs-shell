from typing import Any

from ignis.widgets import Box, Label, Scale
from ignis.services.audio import AudioService, Stream
from ignis.services.backlight import BacklightService

from exs_shell import register
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.state import State


@register.event
class Rollers(Box):
    def __init__(self, scale: float, **kwargs: Any):
        self.scale = scale
        self.backlight: BacklightService = State.services.backlight
        self.audio: AudioService = State.services.audio
        self.audio_scale = Scale(
            value=self.audio.speaker.volume,  # type: ignore
            min=0,
            max=100,
            on_change=lambda _: self.audio.speaker.set_volume(_.value),  # type: ignore
            css_classes=["control-center-rollers-audio-scale"],
            hexpand=True,
        )
        self.audio_icon = Label(
            label=Icons.volume.mapping(self.audio.speaker.volume),  # type: ignore
            css_classes=["control-center-rollers-audio-icon"],
        )
        self.audio_space = Box(
            child=[self.audio_icon, self.audio_scale],
            css_classes=["control-center-rollers-audio-container"],
        )
        self.mic_scale = Scale(
            value=self.audio.microphone.volume,  # type: ignore
            min=0,
            max=100,
            on_change=lambda _: self.audio.microphone.set_volume(_.value),  # type: ignore
            css_classes=["control-center-rollers-mic-scale"],
            hexpand=True,
        )
        self.mic_icon = Label(
            label=Icons.ui.MIC,
            css_classes=["control-center-rollers-mic-icon"],
        )
        self.mic_space = Box(
            child=[self.mic_icon, self.mic_scale],
            css_classes=["control-center-rollers-mic-container"],
        )
        self.backlight_scale = Scale(
            value=self.backlight.brightness,
            min=0,
            max=self.backlight.max_brightness,
            on_change=lambda _: self.backlight.set_brightness(_.value),
            css_classes=["control-center-rollers-backlight-scale"],
            hexpand=True,
        )
        self.backlight_icon = Label(
            label=Icons.backlight.mapping(self.backlight.brightness),  # type: ignore
            css_classes=["control-center-rollers-backlight-icon"],
        )
        self.backlight_space = Box(
            child=[self.backlight_icon, self.backlight_scale],
            css_classes=["control-center-rollers-backlight-container"],
        )
        super().__init__(
            vertical=True,
            child=[self.audio_space, self.mic_space, self.backlight_space],
            spacing=3 * self.scale,
            css_classes=["control-center-rollers"],
        )

    @register.events.audio("notify::volume", "speaker")
    @register.events.audio("notify::is-muted", "speaker")
    def __on_volume(self, stream: Stream, *_: Any):
        if stream.is_muted:
            self.audio_icon.label = Icons.volume.MUTED
            self.audio_scale.set_value(0)
        else:
            self.audio_icon.label = Icons.volume.mapping(stream.volume)  # type: ignore
            self.audio_scale.set_value(stream.volume)  # type: ignore

    @register.events.audio("notify::volume", "microphone")
    @register.events.audio("notify::is-muted", "microphone")
    def __on_microphone(self, stream: Stream, *_: Any):
        if stream.is_muted:
            self.mic_scale.set_value(0)
        else:
            self.mic_scale.set_value(stream.volume)  # type: ignore

    @register.events.backlight("notify::brightness")
    def __on_brightness(self, backlight: BacklightService, *_: Any):
        self.backlight_icon.label = Icons.backlight.mapping(backlight.brightness / 1000)  # type: ignore
        self.backlight_scale.set_value(backlight.brightness)
