from enum import StrEnum

from ignis.services.network import WifiAccessPoint


class WifiIcons(StrEnum):
    CONNECTED = "network_wifi"
    DISCONNECTED = "signal_wifi_off"
    CONNECTING = "signal_wifi_4_bar_lock"
    DISABLED = "signal_wifi_off"
    GENERIC = "network_wifi_locked"
    STRENGTH_1 = "network_wifi_1_bar"
    STRENGTH_2 = "network_wifi_2_bar"
    STRENGTH_3 = "network_wifi_3_bar"
    STRENGTH_4 = "network_wifi"
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

    @classmethod
    def get_icon_ap(cls, ap: WifiAccessPoint):
        is_secured = ap.security
        strength = ap.strength

        if strength > 75:
            base_name = cls.STRENGTH_3
        elif strength > 50:
            base_name = cls.STRENGTH_2
        elif strength > 25:
            base_name = cls.STRENGTH_1
        else:
            base_name = cls.STRENGTH_4

        if is_secured:
            return f"{base_name}_locked"
        else:
            return base_name
