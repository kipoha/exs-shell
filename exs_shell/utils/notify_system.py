import tempfile
import subprocess
from typing import Literal
from PIL import Image


def create_color_icon(color: str, size: int = 1) -> str:
    image = Image.new("RGB", (size, size), color)
    temp_file = tempfile.NamedTemporaryFile(suffix=".png")
    image.save(temp_file.name)
    return temp_file.name


def send_notification(
    summary: str,
    body: str = "",
    app_name: str = "Exs Shell",
    urgency: Literal["low", "normal", "critical"] = "normal",
    icon: str | None = None,
    color_icon: str | None = None,
    replace_id: int | None = None,
) -> None:
    cmd = ["dunstify", "-a", app_name, "-u", urgency]

    temp_icon_path = None

    if color_icon:
        temp_icon_path = create_color_icon(color_icon)
        cmd += ["-i", temp_icon_path]
    elif icon:
        cmd += ["-i", icon]

    if replace_id:
        cmd += ["-r", str(replace_id)]

    cmd += [summary, body]

    subprocess.Popen(cmd)
