from window.settings.elements import (
    SettingsPage,
    SettingsRow,
    SettingsEntry,
    SettingsGroup,
)
from ignis import utils
from ignis import widgets
from ignis.services.fetch import FetchService
from ignis._version import __version__
from config.user import options as user_options

fetch = FetchService.get_default()


def get_os_logo() -> str | None:
    logo = fetch.os_logo_text_dark or fetch.os_logo_dark or fetch.os_logo
    return logo


class AboutEntry(SettingsEntry):
    def __init__(self):
        page = SettingsPage(
            name="System info",
            groups=[
                widgets.Icon(
                    icon_name=fetch.os_logo,
                    pixel_size=200,
                ),
                SettingsGroup(
                    name="Info",
                    rows=[
                        SettingsRow(label="OS", sublabel=fetch.os_name),
                        SettingsRow(label="Ignis version", sublabel=__version__),
                        SettingsRow(label="Session type", sublabel=fetch.session_type),
                        SettingsRow(
                            label="Wayland compositor", sublabel=fetch.current_desktop
                        ),
                        SettingsRow(label="Kernel", sublabel=fetch.kernel),
                        SettingsRow(label="Hostname", sublabel=fetch.hostname),
                        SettingsRow(label="CPU", sublabel=fetch.cpu),
                        SettingsRow(
                            label="Uptime",
                            sublabel=utils.Poll(
                                60_000,
                                lambda _: f"{fetch.uptime[0]} Days, {fetch.uptime[1]} Hours, {fetch.uptime[2]} Minutes",
                            ).bind("output"),
                        ),
                    ],
                ),
            ],
        )
        super().__init__(
            label="System info",
            icon="",
            page=page,
        )
