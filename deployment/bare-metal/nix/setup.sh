#!/usr/bin/env bash

# Load OS meta
if ! . "deployment/bare-metal/nix/load_os_meta.sh"; then
  echo "Failed to match supported OS. Halting execution."
  return 1
fi

# TODO: Only collect inputs from user and run config setup if the .env file does not exist

# Collect inputs from the user
. "deployment/bare-metal/nix/collect_inputs.sh"

# Prepare the system for the project
# shellcheck source=deployment/bare-metal/linux/debian/prepare.sh
. "deployment/bare-metal/$PDACLI_PLATFORM/$PDACLI_DISTRO/prepare.sh"

# Setup the environment and yaml configuration files
. "deployment/bare-metal/nix/setup_config.sh"

echo ""
echo "The environment is ready to run!"
echo ""
echo "Please run the \"pda\" command to get started."
echo ""
