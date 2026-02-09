# exs-shell

## Showcase
no showcase
<!-- <div align="center"> -->
<!-- <img src="assets/1.png" width="550"> -->
<!-- <img src="assets/2.png" width="550"> -->
<!-- <img src="assets/3.png" width="550"> -->
<!-- <img src="assets/4.png" width="550"> -->
<!-- <img src="assets/5.png" width="550"> -->
<!-- <img src="assets/6.png" width="550"> -->
<!-- <img src="assets/7.png" width="550"> -->
<!-- </div> -->
<!-- <br /><br /> -->


## Installation

> [!WARNING]
> This shell working only for **Niri Wayland Compositor**.  
> And Shell in progress.

## Dependencies
```
jetbrains mono nerd-font
dart-sass
swww
dunst
```
1. Installing
Only one script
```bash
curl -fsSl https://raw.githubusercontent.com/kipoha/exs-shell/refs/heads/main/scripts/install.sh | bash
```

or


Clone and install
```bash
git clone https://github.com/kipoha/exs-shell.git
cd exs-shell
chmod +x scripts/install.sh
./scripts/install.sh
```

or install for development
```bash
git clone https://github.com/kipoha/exs-shell.git
cd exs-shell
chmod +x scripts/install-dev.sh
./scripts/install-dev.sh
```


2. Verify installation:
```bash
which exs
```

3. Quick `ipc` command(Optional):
If you have a separate script for fast commands like brightness control:
```bash
exs ipc launcher toggle
```

Use to see all commands
```exs -h```
