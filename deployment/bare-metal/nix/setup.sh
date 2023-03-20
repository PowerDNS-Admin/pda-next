#!/usr/bin/env bash

# Load OS meta
if ! . "deployment/bare-metal/nix/load_os_meta.sh"; then
  echo "Failed to match supported OS. Halting execution."
  return 1
fi

# Load the default environment configuration values
source ".env.tpl"

PDACLI_BUILD_CONF=${PDACLI_BUILD_CONF:-''}
PDACLI_PREPARE_ENV=${PDACLI_PREPARE_ENV:-'1'}
PDACLI_LOAD_ENV=${PDACLI_LOAD_ENV:-'1'}
PDA_ENV_FILE=${PDA_ENV_FILE:-'.env'}
PDA_ENV_FILE_ENCODING=${PDA_ENV_FILE_ENCODING:-'UTF-8'}
PDA_ENV_SECRETS_DIR=${PDA_ENV_SECRETS_DIR:-'/run/secrets'}

if [[ "$PDACLI_BUILD_CONF" == '' ]] && [[ ${#PDA_ENV_FILE} -gt 0 ]] && [ ! -f "$PDA_ENV_FILE" ]; then
  PDACLI_BUILD_CONF='1'
fi

# Collect inputs from the user if the configuration builder has been activated
if [[ "$PDACLI_BUILD_CONF" == '1' ]]; then
  . "deployment/bare-metal/nix/collect_inputs.sh"
else
  echo "Skipping configuration builder."
fi

# Prepare the system for the project using an OS specific script if it exists, otherwise use a distribution script
if [ -f "deployment/bare-metal/$PDACLI_PLATFORM/$PDACLI_OS.sh" ]; then
  # shellcheck source=deployment/bare-metal/linux/debian.sh
  . "deployment/bare-metal/$PDACLI_PLATFORM/$PDACLI_OS.sh"
else
  # shellcheck source=deployment/bare-metal/linux/debian.sh
  . "deployment/bare-metal/$PDACLI_PLATFORM/$PDACLI_DISTRO.sh"
fi

# Setup the environment and yaml configuration files if the configuration builder has been activated
if [[ "$PDACLI_BUILD_CONF" == '1' ]]; then
  . "deployment/bare-metal/nix/create_config.sh"
fi

# shellcheck source=.env.tpl
[ -f "$PDA_ENV_FILE" ] && . "$PDA_ENV_FILE"

echo ""
echo "The environment is ready to run!"
echo ""
echo "Please run the \"pda\" command to get started."
echo ""
