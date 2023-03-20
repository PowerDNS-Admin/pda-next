#!/usr/bin/env bash

# Load OS meta
if ! . "deployment/bare-metal/nix/load_os_meta.sh"; then
  echo "Failed to match supported OS. Halting execution."
  return 1
fi

# Collect inputs from the user before preparing the environment
. "deployment/bare-metal/nix/collect_inputs.sh"

# Prepare the system for the project using an OS specific script if it exists, otherwise use a distribution script
if [ -f "deployment/bare-metal/$PDACLI_PLATFORM/$PDACLI_OS.sh" ]; then
  # shellcheck source=deployment/bare-metal/linux/debian.sh
  . "deployment/bare-metal/$PDACLI_PLATFORM/$PDACLI_OS.sh"
else
  # shellcheck source=deployment/bare-metal/linux/debian.sh
  . "deployment/bare-metal/$PDACLI_PLATFORM/$PDACLI_DISTRO.sh"
fi

echo ""
echo "The environment is ready to run!"
echo ""
echo "Please run the \"pda\" command to get started."
echo ""
echo "For more information, please visit:"
echo "https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/deployment/README.md"
echo ""
