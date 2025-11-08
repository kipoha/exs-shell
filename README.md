## Installation
Installs the package and dependencies globally (the exs-shell command will be available in your PATH):
```bash
sudo pip install git+https://github.com/kipoha/exs-shell.git --break-system-packages
```

## Installation(for development)
1. Clone the repository:
```bash
git clone https://github.com/kipoha/exs-shell.git
cd exs-shell
```

2. Install globally:

Standard installation
Installs the package and dependencies globally (the exs-shell command will be available in your PATH):
```bash
sudo pip install . --break-system-packages
```

Editable installation (for development)
Allows you to make changes to the source code and see them immediately in the installed version:
```bash
sudo pip install -e . --break-system-packages
```

> [!WARNING]
> `--break-system-packages` is required on some Linux distributions (e.g., Arch)
> to allow pip to work with system-wide packages.

3. Verify installation:
```bash
which exs-shell
which exs-ipc
```

4. Quick `ipc` command(Optional):
If you have a separate script for fast commands like brightness control:
```bash
exs-ipc brightness-up
```
