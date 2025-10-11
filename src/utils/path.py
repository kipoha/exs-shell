import os
import sys
from pathlib import Path
from gi.repository import GLib  # type: ignore


class PathUtils:
    root: Path = Path(__file__).parent.parent.parent
    path: Path = root / "src"
    assets_path: Path = path / "assets"

    @classmethod
    def generate_path(cls, path_name: str | list[str], base_path: Path | None = None) -> str:
        base_path = base_path or cls.path
        if isinstance(path_name, list):
            path_name = "/".join(path_name)
        p = str(base_path / path_name)
        return p


is_sphinx_build: bool = "sphinx" in sys.modules


class Dirs:
    TEMP_DIR = "/tmp/exs-shell"
    CACHE_DIR = (
        f"{GLib.get_user_cache_dir()}/exs-shell"
        if not is_sphinx_build
        else "$XDG_CACHE_HOME/ignis"
    )
    DATA_DIR = (
        f"{GLib.get_user_data_dir()}/exs-shell"
        if not is_sphinx_build
        else "$XDG_DATA_HOME/ignis"
    )

    @classmethod
    def ensure_dirs_exist(cls) -> None:
        for directory in (cls.TEMP_DIR, cls.CACHE_DIR, cls.DATA_DIR):
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                print(f"[WARN] Failed to create directory {directory}: {e}")
