from pathlib import Path


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
