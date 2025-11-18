#!/bin/bash

sudo mkdir -p /opt/exs-shell
sudo python -m venv /opt/exs-shell
sudo /opt/exs-shell/bin/pip install --upgrade git+https://github.com/kipoha/exs-shell.git
sudo ln -s /opt/exs-shell/bin/exs-shell /usr/local/bin/exs-shell
sudo ln -s /opt/exs-shell/bin/exs-ipc /usr/local/bin/exs-ipc
