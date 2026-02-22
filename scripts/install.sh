#!/bin/bash
set -e

REPO="kipoha/exs-shell"

echo "Fetching releases..."

mapfile -t TAGS < <(
    curl -s "https://api.github.com/repos/$REPO/releases" |
    grep '"tag_name":' |
    sed -E 's/.*"([^"]+)".*/\1/'
)

if [ ${#TAGS[@]} -eq 0 ]; then
    echo "No releases found"
    exit 1
fi

echo "Available releases:"
for i in "${!TAGS[@]}"; do
    printf "[%d] %s\n" "$((i+1))" "${TAGS[$i]}"
done

read -r -p "Select version [1]: " choice < /dev/tty
choice=${choice:-1}

# Проверка что введено число
if ! [[ "$choice" =~ ^[0-9]+$ ]]; then
    echo "Invalid selection"
    exit 1
fi

index=$((choice-1))

if [ "$index" -ge "${#TAGS[@]}" ]; then
    echo "Selection out of range"
    exit 1
fi

VERSION="${TAGS[$index]}"

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
