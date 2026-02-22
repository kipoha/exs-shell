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
from exs_shell.interfaces.enums.colorschemes import ColorSchemes


class Matugen:
    @staticmethod
    def update() -> None:
        scheme = (
            "tonal-spot" if appearance.scheme not in ColorSchemes else appearance.scheme
        )
        cmds: list[str] = [
            SCB.matugen(appearance.wallpaper_path, scheme, appearance.dark, appearance.contrast),
            SCB.gsettings(appearance.dark),
        ]
        for cmd in cmds:
            run_async_task(exec_sh_async(cmd))
        Matugen.update_previews()
        Matugen.reload_css()

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
                    appearance.contrast,
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

            scss_file = Dirs.CONFIG_DIR / "palettes.scss"
            scss_file.write_text(scss)

        run_async_task(do())
        Matugen.reload_css()

    @staticmethod
    def reload_css():
        def do():
            css_manager = CssManager.get_default()
            css_manager.reload_all_css()

        Timeout(ms=3000, target=do)
