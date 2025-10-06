from typing import Self


class SingletonClass:
    _instance: Self | None = None

    @classmethod
    def get_default(cls) -> Self:
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
