#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root"
    exit 1
fi

REPO="kipoha/exs-shell"
echo "Fetching releases..."
RELEASES=$(curl -s "https://api.github.com/repos/$REPO/releases" | \
           grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$RELEASES" ]; then
    echo "Failed to fetch releases"
    exit 1
fi

i=1
declare -a TAGS
echo "Available releases:"
while read -r tag; do
    echo "[$i] $tag"
    TAGS[$i]="$tag"
    i=$((i+1))
done <<< "$RELEASES"

read -p "Enter the number of the version to install (default latest = 1): " choice
choice=${choice:-1}
VERSION="${TAGS[$choice]}"
echo "Selected version: $VERSION"

mkdir -p /opt/exs-shell
python -m venv /opt/exs-shell
/opt/exs-shell/bin/pip install --upgrade "git+https://github.com/$REPO.git@$VERSION"

create_symlink() {
    local target="$1"
    local link="$2"

    if [ -L "$link" ] || [ -e "$link" ]; then
        rm -f "$link"
    fi

    ln -s "$target" "$link"
}

create_symlink "/opt/exs-shell/bin/exs" "/usr/local/bin/exs"

echo "Installation complete!"
