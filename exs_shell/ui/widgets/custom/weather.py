import requests
import traceback

from typing import Any

from loguru import logger

from ignis.widgets import Label

from exs_shell import register
from exs_shell.configs.user import weather
from exs_shell.utils.loop import run_in_thread


@register.event
@register.widget
class WeatherLabel(Label):
    def __init__(self, **kwargs: Any):
        super().__init__(label="", **kwargs)

    @run_in_thread
    def update(self, *_: Any):
        weather = self.fetch_weather()
        self.set_label(weather)
        "⛅️ +1°C"

    @register.events.option(weather, "location")
    @register.events.option(weather, "farenheit")
    @register.events.poll(10 * 60 * 1000)  # 10 minutes
    def update_label(self):
        self.update()

    def fetch_weather(self) -> str:
        try:
            params = {
                "format": "%c %t",
                "location": weather.location or "",
            }
            if weather.farenheit:
                params["u"] = ""
            r = requests.get("https://wttr.in/", params=params, timeout=10)
            return r.text.strip()
        except Exception:
            logger.error(traceback.format_exc())
            return "N/A"
