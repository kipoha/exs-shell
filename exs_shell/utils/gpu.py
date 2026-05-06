from pyudev import Context


def get_all_gpus() -> list[tuple[str, str]]:
    context = Context()
    gpus = []
    for device in context.list_devices(
        subsystem="pci", ID_PCI_CLASS_FROM_DATABASE="Display controller"
    ):
        model = device.get("ID_MODEL_FROM_DATABASE") or device.get("ID_MODEL")
        vendor = device.get("ID_VENDOR_FROM_DATABASE") or device.get("ID_VENDOR")
        gpus.append((vendor, model))

    return gpus
