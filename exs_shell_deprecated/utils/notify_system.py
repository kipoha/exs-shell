import subprocess
from typing import Literal
from PIL import Image
import tempfile


def create_color_icon(color: str, size: int = 1) -> str:
    image = Image.new("RGB", (size, size), color)
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    image.save(temp_file.name)
    return temp_file.name


def execute_send_notification(
    summary: str,
    body: str = "",
    app_name: str = "Notifier",
    urgency: Literal["low", "normal", "critical"] = "normal",
    icon: str | None = None,
    color_icon: str | None = None,
    replace_id: int | None = None,
):
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


def send_notification(
    summary: str,
    body: str = "",
    urgency: Literal["low", "normal", "critical"] = "normal",
    icon: str | None = None,
    color_icon: str | None = None,
    replace_id: int | None = None,
):
    execute_send_notification(
        summary=summary,
        body=body,
        app_name="Exs Shell",
        urgency=urgency,
        icon=icon,
        color_icon=color_icon,
        replace_id=replace_id,
    )
