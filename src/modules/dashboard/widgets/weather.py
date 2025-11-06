import requests

from ignis import widgets, utils

from config.user import options


class Weather(widgets.Overlay):
    def __init__(self):
        background = widgets.Box(
            css_classes=["dashboard-widget-weather-bg"]
        )

        icon = widgets.Label(
            label="󰖐",
            css_classes=["dashboard-widget-weather-icon"],
        )

        temp = widgets.Label(
            label=utils.Poll(600_000, self.fetch_weather).bind("output"),
            css_classes=["dashboard-widget-weather-temp"],
        )

        super().__init__(
            child=background,
            overlays=[icon, temp],
            css_classes=["dashboard-widget-weather"],
        )

        options.weather.connect_option("location", self.fetch_weather)
        options.weather.connect_option("farenheit", self.fetch_weather)

    def fetch_weather(self, *_):
        try:
            params = {
                "format": "%t",
                "location": options.weather.location,
            }
            if options.weather.farenheit:
                params["u"] = ""
            r = requests.get("https://wttr.in/", params=params, timeout=5)
            return r.text.strip()
        except Exception:
            return "N/A"
