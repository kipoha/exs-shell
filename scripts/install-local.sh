#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root"
    exit 1
fi

mkdir -p /opt/exs-shell
python -m venv /opt/exs-shell
/opt/exs-shell/bin/pip install .


create_symlink() {
    local target="$1"
    local link="$2"

    if [ -L "$link" ] || [ -e "$link" ]; then
        rm -f "$link"
    fi

    ln -s "$target" "$link"
}

create_symlink "/opt/exs-shell/bin/exs" "/usr/local/bin/exs"
