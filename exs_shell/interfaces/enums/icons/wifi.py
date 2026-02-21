from enum import StrEnum


class WifiIcons(StrEnum):
    CONNECTED = "wifi_tethering"
    DISCONNECTED = "wifi_tethering_error"
    CONNECTING = "signal_wifi_4_bar_lock"
    DISABLED = "portable_wifi_off"
    GENERIC = "wifi_lock"
    STRENGTH_0 = "signal_wifi_0_bar"
    STRENGTH_1 = "network_wifi_1_bar"
    STRENGTH_2 = "network_wifi_2_bar"
    STRENGTH_3 = "network_wifi"
    STRENGTH_4 = "signal_wifi_4_bar"
    # CONNECTED = "󰤨"
    # DISCONNECTED = "󰤩"
    # CONNECTING = "󰤪"
    # DISABLED = "󰤭"
    # GENERIC = "󰤬"
    # STRENGTH_0 = "󰤯"
    # STRENGTH_1 = "󰤟"
    # STRENGTH_2 = "󰤢"
    # STRENGTH_3 = "󰤥"
    # STRENGTH_4 = "󰤨"
