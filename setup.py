from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
import os
import subprocess

HERE = os.path.dirname(__file__)
IDLE_DIR = os.path.join(HERE, "exs_shell", "extensions", "idle")

class build_idle_py(_build_py):
    def run(self):
        super().run()
        out = os.path.join(IDLE_DIR, "wl_idle_helper")
        print("Building wl_idle_helper in-place...")
        subprocess.check_call([
            "gcc",
            os.path.join(IDLE_DIR, "wl_idle_helper.c"),
            os.path.join(IDLE_DIR, "ext-idle-notify-v1-protocol.c"),
            "-o", out,
            "-lwayland-client",
            "-lm",
        ])
        print("Done:", out)

setup(
    name="exs-shell",
    packages=["exs_shell", "exs_shell.extensions.idle"],
    include_package_data=True,
    cmdclass={"build_py": build_idle_py},
)
