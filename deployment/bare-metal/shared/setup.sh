#!/usr/bin/env bash

# Load OS meta
if ! . "deployment/bare-metal/linux/shared/load_os_meta.sh"; then
  echo "Failed to match supported OS. Halting execution."
  return 1
fi

# Load CLI variables
# shellcheck source=deployment/bare-metal/linux/debian/vars.sh
. "deployment/bare-metal/$PDACLI_PLATFORM/$PDACLI_DISTRO/vars.sh"

# Collect input from the user
# shellcheck source=deployment/bare-metal/linux/debian/inputs.sh
. "deployment/bare-metal/$PDACLI_PLATFORM/$PDACLI_DISTRO/inputs.sh"

# Prepare the system for the project
# shellcheck source=deployment/bare-metal/linux/debian/prepare.sh
. "deployment/bare-metal/$PDACLI_PLATFORM/$PDACLI_DISTRO/prepare.sh"

# Setup the environment and yaml configuration files
. "deployment/bare-metal/linux/shared/setup_config.sh"

echo ""
echo "The environment is ready to run!"
echo ""
echo "Please run the \"pda\" command to get started."
echo ""

export PDACLI_DISTRO
