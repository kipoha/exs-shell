from enum import StrEnum


class WifiIcons(StrEnum):
    CONNECTED = "network_wifi"
    DISCONNECTED = "signal_wifi_off"
    CONNECTING = "signal_wifi_4_bar_lock"
    DISABLED = "signal_wifi_off"
    GENERIC = "network_wifi_locked"
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
