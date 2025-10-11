from typing import Any


def osd_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:
    from modules.osd import OSD

    osd = OSD.get_default()
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "volume-up": (osd, "update_volume", {"up": True}, "Volume Up"),
        "volume-down": (osd, "update_volume", {"up": False}, "Volume Down"),
        "toggle-mute": (osd, "toggle_mute", {}, "Volume Mute"),
        "brightness-up": (osd, "update_brightness", {"up": True}, "Brightness Up"),
        "brightness-down": (osd, "update_brightness", {"up": False}, "Brightness Down"),
    }

    return cmds
