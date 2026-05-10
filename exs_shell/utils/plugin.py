from collections.abc import Sequence
from pathlib import Path
import re
import subprocess
import sys
import tomllib

from libexs.utils import plugin as pl_core

from exs_shell.app.path import Dirs
from exs_shell.configs.user import user
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
        pl_path = Dirs.PLUGINS_DIR / repo_name
        _clone(name_url, pl_path)
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
        pl_path = Dirs.PLUGINS_DIR / name_url
        _clone(repo, pl_path)

    if pl_path.exists():
        for dep in _fetch_dependencies(pl_path):
            if not (Dirs.PLUGINS_DIR / dep).exists():
                _clone(f"{repo_url}/{dep}", Dirs.PLUGINS_DIR / dep)

    _update()
    print(f"Plugin '{plugin_name}' installed")


def _fetch_index() -> AnyDict:
    import urllib.request

    url = "https://raw.githubusercontent.com/exs-lab/exs-plugins/main/index.toml"
    with urllib.request.urlopen(url) as r:
        return tomllib.loads(r.read().decode())


def _fetch_dependencies(path: Path) -> Sequence[str]:
    pl = path / "plugin.toml"
    if not pl.exists():
        return []
    with open(pl, "rb") as f:
        return tomllib.load(f).get("plugin", {}).get("dependencies", [])


def _find_dependents(name: str) -> list[str]:
    dependents = []
    for pl in Dirs.PLUGINS_DIR.iterdir():
        if pl.name == name:
            continue
        if name in _fetch_dependencies(pl):
            dependents.append(pl.name)
    return dependents


def _clone(url: str, dest: Path) -> None:
    subprocess.run(["git", "clone", url, str(dest)], check=True)


def _update():
    subprocess.Popen(["exs", "ipc", "plugin", "update"], stdout=subprocess.DEVNULL)


def remove(name: str, _removing: set[str] | None = None) -> None:
    dest = Dirs.PLUGINS_DIR / name
    if not dest.exists():
        print(f"Plugin '{name}' not found")
        return
    if str(dest) in user.plugins:
        print(f"Plugin '{name}' is enabled\nDisable it first")
        return

    _removing = _removing or {name}

    dependents = [d for d in _find_dependents(name) if d not in _removing]
    if dependents:
        print(f"Plugin '{name}' is required by: {', '.join(dependents)}")
        answer = input("Remove them too? [y/N] ").strip().lower()
        if answer != "y":
            print(f"Plugin '{name}' not removed")
            return
        _removing.update(dependents)
        for dep in dependents:
            remove(dep, _removing)

    subprocess.run(["rm", "-rf", str(dest)], check=True)
    _update()
    print(f"Plugin '{name}' removed")


def list():
    print("Installed plugins:")
    for pl in Dirs.PLUGINS_DIR.iterdir():
        if pl_core.check(pl):
            print(f"- {pl.name}")


def new(name: str):
    dest = Dirs.PLUGINS_DIR / name
    if dest.exists():
        print(f"Plugin '{name}' already exists")
        return
    subprocess.run(
        [
            sys.executable,
            "-m",
            "cookiecutter",
            "https://github.com/exs-lab/exs-plugin-template",
            "--no-input",
            f"name={name}",
            "--output-dir",
            str(Dirs.PLUGINS_DIR),
        ],
        check=True,
    )
    print(f"Plugin '{name}' created")
    _update()
