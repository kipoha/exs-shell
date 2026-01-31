from typing import Self


class SingletonClass:
    _instance: Self | None = None

    @classmethod
    def get_default(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
