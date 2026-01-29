import os
import sys
from pathlib import Path
from gi.repository import GLib  # type: ignore


is_sphinx_build: bool = "sphinx" in sys.modules
dir_name: str = "exs_shell"


class Paths:
    root: Path = Path(__file__).parent.parent.parent
    path: Path = root / dir_name
    assets: Path = path / "assets"

    @classmethod
    def generate_path(
        cls, path_name: str | list[str] | Path, base_path: Path | None = None
    ) -> str:
        base_path = base_path or cls.path
        if isinstance(path_name, list):
            path_name = "/".join(path_name)
        p = str(base_path / path_name)
        return p


class Dirs:
    TEMP_DIR: Path = Path("/tmp") / dir_name
    CACHE_DIR: Path = (
        Path(GLib.get_user_cache_dir()) / dir_name
        if not is_sphinx_build
        else Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache")))
        / dir_name
    )
    DATA_DIR: Path = (
        Path(GLib.get_user_data_dir()) / dir_name
        if not is_sphinx_build
        else Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local/share")))
        / dir_name
    )
    CONFIG_DIR: Path = Path.home() / ".config" / dir_name

    @classmethod
    def ensure_dirs_exist(cls) -> None:
        for directory in (cls.TEMP_DIR, cls.CACHE_DIR, cls.DATA_DIR, cls.CONFIG_DIR):
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"[WARN] Failed to create directory {directory}: {e}")
