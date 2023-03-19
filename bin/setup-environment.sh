#!/usr/bin/env bash

# Define system packages required for the project
pkgs=(build-essential libmysqlclient-dev python3 python3-dev python3-venv)

# Add sudo to elevated commands when not running as root already
CMD_PREFIX=
if [ ! "$EUID" -eq 0 ]; then
  CMD_PREFIX=sudo
fi

# Move to the project's root directory if not already there
CURRENT_PATH=$(dirname "$(readlink -f "$0")")
PARENT_DIRECTORY=$(basename $CURRENT_PATH)

if [ "$PARENT_DIRECTORY" == 'bin' ]; then
  cd "$CURRENT_PATH/.."
fi

# Install missing system packages
$CMD_PREFIX apt update
$CMD_PREFIX apt-get -y --ignore-missing install "${pkgs[@]}"

# Load the environment configuration
source .env

# Setup the Python virtual environment
/usr/bin/env python3 -m venv ./venv

# Load the Python virtual environment
source venv/bin/activate

# Install the required pip modules based on the configuration in setup.py
pip install --editable .

echo ""
echo "The environment is ready to build images!"
echo ""
echo "Please run the \"pda\" command to get started."
echo ""