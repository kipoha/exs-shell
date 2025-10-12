from ignis import widgets


def left(monitor_name) -> widgets.Box:
    from modules.bar.childs import modules
    return widgets.Box(
        child=[
            modules["tray"]()
        ],
        spacing=10
    )


def center(monitor_name) -> widgets.Box:
    from modules.bar.childs import modules
    return widgets.Box(
        child=[
            modules["clock"](),
            modules["cava"](),
        ],
        spacing=20
    )


def right(monitor_name) -> widgets.Box:
    from modules.bar.childs import modules
    return widgets.Box(
        child=[
            modules["layout"](),
            modules["battery"](),
        ],
        spacing=10
    )
