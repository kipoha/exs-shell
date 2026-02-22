#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root"
    exit 1
fi

rm -rf /usr/local/bin/exs
rm -rf /opt/exs-shell

echo "Uninstallation complete!"
