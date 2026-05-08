from pathlib import Path
import re
import subprocess
import tomllib

from libexs.utils import plugin as pl_core

from exs_shell.app.path import Dirs
from exs_shell.interfaces.types import AnyDict

git_regex = re.compile(r"^https://github\.com/[\w-]+/[\w-]+$")
repo_url = "https://github.com/exs-lab/exs-plugins"


def install(name_url: str) -> None:
    if git_regex.match(name_url):
        repo_name = name_url.rstrip("/").split("/")[-1]
        plugin_name = repo_name
        if (Dirs.PLUGINS_DIR / repo_name).exists():
            print(f"Plugin '{repo_name}' already installed")
            return
        _clone(name_url, Dirs.PLUGINS_DIR / repo_name)
    else:
        plugin_name = name_url
        index = _fetch_index()
        if name_url not in index["plugins"]:
            print(f"Plugin '{name_url}' not found in registry")
            return
        if (Dirs.PLUGINS_DIR / name_url).exists():
            print(f"Plugin '{name_url}' already installed")
            return
        repo = index["plugins"][name_url]["repo"]
        _clone(repo, Dirs.PLUGINS_DIR / name_url)

    print(f"Plugin '{plugin_name}' installed")


def _fetch_index() -> AnyDict:
    import urllib.request

    url = "https://raw.githubusercontent.com/exs-lab/exs-plugins/main/index.toml"
    with urllib.request.urlopen(url) as r:
        return tomllib.loads(r.read().decode())


def _clone(url: str, dest: Path) -> None:
    subprocess.run(["git", "clone", url, str(dest)], check=True)


def remove(name: str) -> None:
    dest = Dirs.PLUGINS_DIR / name
    if dest.exists():
        subprocess.run(["rm", "-rf", str(dest)], check=True)
        print(f"Plugin '{name}' removed")
    else:
        print(f"Plugin '{name}' not found")


def list():
    print("Installed plugins:")
    for pl in Dirs.PLUGINS_DIR.iterdir():
        if pl_core.check(pl):
            print(f"- {pl.name}")
