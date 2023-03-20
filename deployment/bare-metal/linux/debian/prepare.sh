#!/usr/bin/env bash

# Determine whether sudo needs to be added to commands based whether the current user is root
PDACLI_CMD_PREFIX=
if [ ! "$EUID" -eq 0 ]; then
  PDACLI_CMD_PREFIX=sudo
fi

# Only prepare the environment if the appropriate flag is set
if [[ "$PDACLI_PREPARE_ENV" == '1' ]]; then
  # Define system packages required for the project
  PDACLI_PKGS=(build-essential python3 python3-dev python3-venv)

  # TODO: Add additional system packages to the list based on user input
  #PDACLI_PKGS+=("'package-name1' 'package-name2' 'package-name3'")

  # Install missing system packages
  $PDACLI_CMD_PREFIX apt update
  $PDACLI_CMD_PREFIX apt-get -y --ignore-missing install "${PDACLI_PKGS[@]}"

  # Determine path to env command
  PDACLI_ENV_PATH=$(which env)

  # Setup the Python virtual environment
  $PDACLI_ENV_PATH python3 -m venv venv
else
  echo "Skipping environment preparation."
fi

# Only load the environment if the appropriate flag is set
if [[ "$PDACLI_LOAD_ENV" == '1' ]]; then
  # Load the Python virtual environment
  . venv/bin/activate
else
  echo "Skipping environment loading."
fi

# Only install the required pip modules if the appropriate flags are set
if [[ "$PDACLI_PREPARE_ENV" == '1' ]] && [[ "$PDACLI_LOAD_ENV" == '1' ]]; then
  # Determine path to pip command
  PDACLI_PIP_PATH=$(which pip)

  # Install the required pip modules based on the configuration in setup.py
  $PDACLI_PIP_PATH install --editable .
else
  echo "Skipping pip module installation."
fi
