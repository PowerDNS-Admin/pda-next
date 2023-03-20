#!/usr/bin/env bash

# Load the default environment configuration values
source ".env.tpl"

# Create array to track which environment variables have been set
PDACLI_ENV_VARS_SET=()

get_admin_contact () {
  echo 'Enter the application administrator''s email and then press return ['"$PDA_ADMIN_EMAIL"']:'
  read -r tmp1
  tmp1=$(echo "$tmp1" | xargs)

  echo 'Enter the application administrator''s full name and then press return ['"$PDA_ADMIN_NAME"']:'
  read -r tmp2
  tmp2=$(echo "$tmp2" | xargs)

  if [[ ${#tmp1} -gt 0 ]] && [[ "$tmp1" != "$PDA_ADMIN_EMAIL" ]]; then
    # shellcheck disable=SC2034
    PDA_ADMIN_EMAIL="$tmp1"
    PDACLI_ENV_VARS_SET+=("PDA_ADMIN_EMAIL")
  fi

  if [[ ${#tmp2} -gt 0 ]] && [[ "$tmp2" != "$PDA_ADMIN_NAME" ]]; then
    # shellcheck disable=SC2034
    PDA_ADMIN_NAME="$tmp2"
    PDACLI_ENV_VARS_SET+=("PDA_ADMIN_NAME")
  fi
}

get_app_email () {
  echo 'Enter the from email address to be used when sending error reports and then press return ['"$PDA_ADMIN_FROM_EMAIL"']:'
  read -r tmp
  tmp=$(echo "$tmp" | xargs)

  if [[ ${#tmp} -gt 0 ]] && [[ "$tmp" != "$PDA_ADMIN_FROM_EMAIL" ]]; then
    # shellcheck disable=SC2034
    PDA_ADMIN_FROM_EMAIL="$tmp"
    PDACLI_ENV_VARS_SET+=("PDA_ADMIN_FROM_EMAIL")
  fi
}

get_config_path () {
  echo 'Enter the absolute or relative path to the application''s yaml config file and then press return ['"$PDA_CONFIG_PATH"']:'
  read -r tmp
  tmp=$(echo "$tmp" | xargs)

  if [[ ${#tmp} -gt 0 ]] && [[ "$tmp" != "$PDA_CONFIG_PATH" ]]; then
    # shellcheck disable=SC2034
    PDA_CONFIG_PATH="$tmp"
    PDACLI_ENV_VARS_SET+=("PDA_CONFIG_PATH")
  fi
}

# Collect inputs from the user
get_app_email
get_admin_contact
get_config_path

# Export the environment variables that have been set
for var_name in "${PDACLI_ENV_VARS_SET[@]}"
do
  # shellcheck disable=SC2163
   export "$var_name"
done

export PDACLI_ENV_VARS_SET
