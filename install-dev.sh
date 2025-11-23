#!/bin/bash

sudo mkdir -p /opt/exs-shell
sudo python -m venv /opt/exs-shell
sudo /opt/exs-shell/bin/pip install -e .

create_symlink() {
    local target="$1"
    local link="$2"

    if [ -L "$link" ] || [ -e "$link" ]; then
        sudo rm -f "$link"
    fi

    sudo ln -s "$target" "$link"
}

create_symlink "/opt/exs-shell/bin/exs-shell" "/usr/local/bin/exs-shell"
create_symlink "/opt/exs-shell/bin/exs-ipc" "/usr/local/bin/exs-ipc"
