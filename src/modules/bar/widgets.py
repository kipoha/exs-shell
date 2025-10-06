from ignis import widgets


def left(monitor_name) -> widgets.Box:
    from modules.bar import modules
    return widgets.Box(
        child=[
            # SystemTray(),
            modules["tray"]()
        ],
        spacing=10
    )


def center(monitor_name) -> widgets.Box:
    from modules.bar import modules
    return widgets.Box(
        child=[
            # Clock(),
            modules["clock"](),
        ],
        spacing=20
    )


def right(monitor_name) -> widgets.Box:
    from modules.bar import modules
    return widgets.Box(
        child=[
            # Battery(),
            modules["battery"](),
        ],
        spacing=10
    )
