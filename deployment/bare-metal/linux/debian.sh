#!/usr/bin/env bash

# Define system packages required for the project
PDACLI_PKGS=(build-essential python3 python3-dev python3-venv)

# Add additional packages based on the environment configuration
if [[ "$PDA_ENV_TYPE" == 'production' ]]; then
  # Add Gunicorn packages if the server type is Gunicorn
  if [[ "$PDA_SERVER_TYPE" == 'gunicorn' ]]; then
    PDACLI_PKGS+=(gunicorn)

  # Add Uvicorn packages if the server type is Uvicorn
  elif [[ "$PDA_SERVER_TYPE" == 'uvicorn' ]]; then
    PDACLI_PKGS+=(uvicorn)

  # Add UWSGI packages if the server type is UWSGI
  elif [[ "$PDA_SERVER_TYPE" == 'uwsgi' ]]; then
    PDACLI_PKGS+=(uwsgi uwsgi-plugin-python3)
  fi
fi

# Add MySQL packages if the database engine is MySQL
if [[ "$PDA_DB_ENGINE" == 'mysql' ]]; then
  PDACLI_PKGS+=(libmysqlclient-dev)

# Add PostgreSQL packages if the database engine is PostgreSQL
elif [[ "$PDA_DB_ENGINE" == 'postgres' ]]; then
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
if [[ "$PDA_VENV_ENABLED" == '1' ]]; then
  # Create a Python virtual environment
  $(which env) python3 -m venv "$PDA_VENV_PATH"

  # Activate the Python virtual environment
  . "$PDA_VENV_PATH/bin/activate"
fi

# Install the required pip modules based on the configuration in setup.py
$(which pip) install --editable .
