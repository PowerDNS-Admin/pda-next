#!/usr/bin/env bash

PDACLI_PKGS="${PDACLI_PKGS:-}"

# TODO: Add additional system packages to the list based on user input
#PDACLI_PKGS+=("'package-name1' 'package-name2' 'package-name3'")

# Install missing system packages
$PDACLI_CMD_PREFIX apt update
$PDACLI_CMD_PREFIX apt-get -y --ignore-missing install "${PDACLI_PKGS[@]}"

# Setup the Python virtual environment
$PDACLI_ENV_PATH python3 -m venv venv

# Load the Python virtual environment
source venv/bin/activate

# Install the required pip modules based on the configuration in setup.py
$PDACLI_PIP_PATH install --editable .
