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

read -r -p "Select version [1]: " choice
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
