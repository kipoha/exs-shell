import os
import subprocess

def build_wl_idle_helper():
    here = os.path.dirname(__file__)
    out = os.path.join(here, "wl_idle_helper")
    print("Building wl_idle_helper in-place...")
    subprocess.check_call([
        "gcc",
        os.path.join(here, "wl_idle_helper.c"),
        os.path.join(here, "ext-idle-notify-v1-protocol.c"),
        "-o", out,
        "-lwayland-client",
        "-lm",
    ])
    print("Done:", out)
