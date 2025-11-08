import os
import subprocess

def build_scss(input_file, output_file):
    home = os.path.expanduser("~")
    cmd = [
        "sass",
        f"--load-path={home}/.config/exs-shell/exs_shell",
        input_file,
        output_file,
    ]
    subprocess.run(cmd, check=True)
