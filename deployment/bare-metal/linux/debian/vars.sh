#!/usr/bin/env bash

# Determine whether sudo needs to be added to commands based whether the current user is root
PDACLI_CMD_PREFIX=
if [ ! "$EUID" -eq 0 ]; then
  PDACLI_CMD_PREFIX=sudo
fi

# Determine path to env command
PDACLI_ENV_PATH=$(which env)

# Determine path to pip command
PDACLI_PIP_PATH=$(which pip)

# Define system packages required for the project
PDACLI_PKGS=(build-essential python3 python3-dev python3-venv)

export PDACLI_CMD_PREFIX PDACLI_ENV_PATH PDACLI_PIP_PATH PDACLI_PKGS
