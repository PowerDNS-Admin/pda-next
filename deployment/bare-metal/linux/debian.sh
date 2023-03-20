#!/usr/bin/env bash

# Define system packages required for the project
PDACLI_PKGS=(build-essential python3 python3-dev python3-venv)

# Add additional packages based on the user's input
if [[ "$PDACLI_ENV_TYPE" == 'production' ]]; then
  PDACLI_PKGS+=(gunicorn)
fi

if [[ "$PDACLI_DB_ENGINE" == 'mysql' ]]; then
  PDACLI_PKGS+=(libmysqlclient-dev)
elif [[ "$PDACLI_DB_ENGINE" == 'postgres' ]]; then
  PDACLI_PKGS+=(libpq-dev)
fi

# Determine whether sudo needs to be added to commands based whether the current user is root
PDACLI_CMD_PREFIX=
if [ ! "$EUID" -eq 0 ]; then
  PDACLI_CMD_PREFIX=sudo
fi

# Install missing system packages
$PDACLI_CMD_PREFIX apt update
$PDACLI_CMD_PREFIX apt-get -y --ignore-missing install "${PDACLI_PKGS[@]}"

# Setup Python virtual environment and activate it only if the environment type is development
if [[ "$PDACLI_ENV_TYPE" == 'development' ]]; then
  # Setup the Python virtual environment
  $(which env) python3 -m venv venv

  # Load the Python virtual environment
  . venv/bin/activate
fi

# Install the required pip modules based on the configuration in setup.py
$(which pip) install --editable .
