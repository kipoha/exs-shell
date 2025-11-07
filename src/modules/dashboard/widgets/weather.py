import requests
import threading
from ignis import widgets, utils
from config.user import options


class Weather(widgets.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            valign="center",
            halign="center",
            css_classes=["dashboard-widget-weather"],
        )

        # --- Overlay для иконки и температуры ---
        self.icon = widgets.Label(
            label="󰖐",
            css_classes=["dashboard-widget-weather-icon"],
        )

        self.poller = utils.Poll(600_000, self.fetch_weather)
        self.temp = widgets.Label(
            label=self.poller.bind("output"),
            css_classes=["dashboard-widget-weather-temp"],
        )

        overlay = widgets.Overlay(
            child=self.icon,
            overlays=[self.temp],
            css_classes=["dashboard-widget-weather-overlay"],
        )

        self.append(overlay)

        # --- Реакция на смену настроек ---
        options.weather.connect_option("location", self._threaded_update)
        options.weather.connect_option("farenheit", self._threaded_update)

    # --- Обновление погоды в фоне ---
    def _threaded_update(self, *_):
        thread = threading.Thread(target=self._update_weather, daemon=True)
        thread.start()

    def _update_weather(self):
        new_poller = utils.Poll(600_000, self.fetch_weather)
        self.poller = new_poller
        value = self.fetch_weather()
        self.temp.set_text(value)

    # --- Запрос погоды ---
    def fetch_weather(self, *_):
        try:
            params = {
                "format": "%t",
                "location": options.weather.location or "",
            }
            if options.weather.farenheit:
                params["u"] = ""
            r = requests.get("https://wttr.in/", params=params, timeout=5)
            return r.text.strip()
        except Exception:
            return "N/A"

# import requests
# import threading
# from ignis import widgets, utils
# from config.user import options
#
#
# class Weather(widgets.Overlay):
#     def __init__(self):
#         self.background = widgets.Box(css_classes=["dashboard-widget-weather-bg"])
#
#         self.icon = widgets.Label(
#             label="󰖐",
#             css_classes=["dashboard-widget-weather-icon"],
#         )
#
#         self.poller = utils.Poll(600_000, self.fetch_weather)
#         self.temp = widgets.Label(
#             label=self.poller.bind("output"),
#             css_classes=["dashboard-widget-weather-temp"],
#         )
#
#         super().__init__(
#             child=self.background,
#             overlays=[self.icon, self.temp],
#             css_classes=["dashboard-widget-weather"],
#         )
#
#         options.weather.connect_option("location", self._threaded_update)
#         options.weather.connect_option("farenheit", self._threaded_update)
#
#     def _threaded_update(self, *_):
#         """Запускает пересоздание poller в отдельном потоке"""
#         thread = threading.Thread(target=self._update_weather, daemon=True)
#         thread.start()
#
#     def _update_weather(self):
#         new_poller = utils.Poll(600_000, self.fetch_weather)
#         self.poller = new_poller
#
#         value = self.fetch_weather()
#         self.temp.set_text(value)
#
#     def fetch_weather(self, *_):
#         try:
#             params = {
#                 "format": "%t",
#                 "location": options.weather.location or "",
#             }
#             if options.weather.farenheit:
#                 params["u"] = ""
#
#             r = requests.get("https://wttr.in/", params=params, timeout=5)
#             return r.text.strip()
#         except Exception:
#             return "N/A"
