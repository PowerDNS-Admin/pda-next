#!/usr/bin/env bash

# Set the default path to the environment configuration file to be created
PDA_ENV_FILE=${PDA_ENV_FILE:-.env}

# Define the environment variables to be set in the environment configuration file
PDACLI_ENV_VARS_SET=(
  'PDA_DB_ENGINE'
  'PDA_ENV_TYPE'
  'PDA_SECRET_KEY'
  'PDA_SERVER_TYPE'
  'PDA_VENV_ENABLED'
  'PDA_VENV_PATH'
)

# Generate a new secret_key setting value
# shellcheck disable=SC2034
PDA_SECRET_KEY=$(pda gen_salt -r)

# Create a variable to hold the environment variable settings that will be saved to the .env.dev file
env_data=''
for var_name in "${PDACLI_ENV_VARS_SET[@]}"
do
  env_data+="$var_name='${!var_name}'\n"
done

# Save the environment variables to the .env.dev file
echo -e "$env_data" >> "\n$PDA_ENV_FILE"
