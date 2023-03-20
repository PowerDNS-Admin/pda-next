#!/usr/bin/env bash

# Create an empty placeholder file for the yaml config file if it does not exist
touch "$PDA_CONFIG_PATH"

# Generate a new secret_key setting value
# shellcheck disable=SC2034
PDA_SECRET_KEY=$(pda gen_salt -r)

# Add the secret_key setting to the list of environment variables that have been set
PDACLI_ENV_VARS_SET+=("PDA_SECRET_KEY")

# Create a variable to hold the environment variable settings that will be saved to the .env.dev file
env_data=''
for var_name in "${PDACLI_ENV_VARS_SET[@]}"
do
  env_data+="export $var_name='${!var_name}'\n"
done

# Save the environment variables to the .env.dev file
echo -e "$env_data" > "$PDA_ENV_FILE"
