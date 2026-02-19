import json

from pathlib import Path

from asyncio import gather

from typing import Awaitable

from ignis.css_manager import CssManager
from ignis.utils import AsyncCompletedProcess, Timeout, exec_sh_async

from exs_shell.utils.loop import run_async_task
from exs_shell.utils.path import Dirs
from exs_shell.utils.other import SCB
from exs_shell.configs.user import appearance
from exs_shell.interfaces.enums.colorschemes import ColorSchemes2 as ColorSchemes



class Matugen:
    @staticmethod
    def update() -> None:
        scheme = (
            "tonal-spot" if appearance.scheme not in ColorSchemes else appearance.scheme
        )
        cmd = SCB.matugen(appearance.wallpaper_path, scheme, appearance.dark)
        run_async_task(exec_sh_async(cmd))
        Timeout(ms=3000, target=Matugen.reload_css)

    @staticmethod
    def update_previews() -> None:
        async def do():
            path = Path(appearance.wallpaper_path)
            if not path.exists():
                return
            scss: str = ""

            tasks: list[Awaitable[AsyncCompletedProcess]] = []
            schemes = list(ColorSchemes)
            for scheme in schemes:
                cmd = SCB.matugen(
                    appearance.wallpaper_path,
                    scheme,
                    appearance.dark,
                    "--json",
                    "hex",
                    "--dry-run",
                )
                tasks.append(exec_sh_async(cmd))

            results = await gather(*tasks)
            for i, result in enumerate(results):
                prefix = schemes[i]
                scss += f"/* {prefix} */\n"
                colors = (
                    json.loads(result.stdout).get("colors", {}) if result.stdout else {}
                )
                if colors:
                    for key, value in colors.items():
                        scss += f"$palette_{prefix.replace('-', '_')}_{key}: {value['default']};\n"
                scss += "\n"

            scss_file = Dirs.CONFIG_DIR / "exs-shell" / "palettes.scss"
            scss_file.write_text(scss)

    @staticmethod
    def reload_css():
        css_manager = CssManager.get_default()
        css_manager.reload_all_css()
