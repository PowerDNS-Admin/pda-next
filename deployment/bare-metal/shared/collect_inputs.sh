#!/usr/bin/env bash

PDACLI_AUTOSTART_DEF='1'
PDACLI_DB_ENGINE_DEF='sqlite'
PDACLI_ENV_TYPE_DEF='production'
PDACLI_SERVER_TYPE_DEF='gunicorn'
PDACLI_VENV_ENABLED_DEF=0
PDACLI_VENV_PATH_DEF='venv'

PDACLI_AUTOSTART=${PDACLI_AUTOSTART:-"$PDACLI_AUTOSTART_DEF"}
PDA_DB_ENGINE=${PDA_DB_ENGINE:-"$PDACLI_DB_ENGINE_DEF"}
PDA_ENV_TYPE=${PDA_ENV_TYPE:-"$PDACLI_ENV_TYPE_DEF"}
PDA_SERVER_TYPE=${PDA_SERVER_TYPE:-"$PDACLI_SERVER_TYPE_DEF"}
PDA_VENV_ENABLED=${PDA_VENV_ENABLED:-"$PDACLI_VENV_ENABLED_DEF"}
PDA_VENV_PATH=${PDA_VENV_PATH:-"$PDACLI_VENV_PATH_DEF"}

# Display the environment configuration
display_configuration() {
  get_yes_no_label "$PDACLI_AUTOSTART"
  local autostart="$YNLR"
  get_yes_no_label "$PDA_VENV_ENABLED"
  local venv_enabled="$YNLR"

  echo "Environment Configuration:"
  echo "  - Setup Auto Start: $autostart"
  echo "  - Environment Type: $PDA_ENV_TYPE"
  echo "  - Database Engine: $PDA_DB_ENGINE"
  echo "  - Server Type: $PDA_SERVER_TYPE"
  echo "  - Virtual Environment Enabled: $venv_enabled"
  if [[ "$PDA_VENV_ENABLED" == "1" ]]; then
    echo "  - Virtual Environment Path: $PDA_VENV_PATH"
  fi
  echo ""
}

get_yes_no_label() {
  # Get the default value from the function arguments
  local test_value="${1-''}"
  YNLR=''

  # Strip leading and trailing whitespace
  test_value=$(echo "$test_value" | xargs)

  # Provide conversion of true / false like values to friendly labels
  if [[ "$test_value" == "1" ]] || [[ "$test_value" == "t" ]] || [[ "$test_value" == "true" ]] ||
    [[ "$test_value" == "y" ]] || [[ "$test_value" == "yes" ]]; then
    YNLR='Yes'
    return 0
  elif [[ "$test_value" == "0" ]] || [[ "$test_value" == "f" ]] || [[ "$test_value" == "false" ]] ||
    [[ "$test_value" == "n" ]] || [[ "$test_value" == "no" ]]; then
    YNLR='No'
    return 0
  fi

  return 1
}

get_yes_no_answer() {
  # Get the default value, prompt, and explanation from the function arguments
  local default_value="${1-'1'}"
  local prompt="${2-''}"
  local explanation="${3-''}"
  YNAR="$default_value"

  # Strip leading and trailing whitespace
  default_value=$(echo "$default_value" | xargs)
  prompt=$(echo "$prompt" | xargs)
  explanation=$(echo "$explanation" | xargs)

  # Provide conversion of true / false like values to friendly labels
  get_yes_no_label "$default_value"
  value_label="$YNLR"

  # Display the prompt and explanation if provided
  echo -e "$prompt\n"
  echo "  1) Yes"
  echo "  2) No"
  echo ""

  if [[ "$explanation" != "" ]]; then
    echo "$explanation"
    echo ""
  fi

  echo "Enter your selection and then press return ['$value_label']:"

  # Read the user input
  read -r tmp

  # Strip leading and trailing whitespace
  tmp=$(echo "$tmp" | xargs)

  # Convert to lowercase
  tmp=$(echo "$tmp" | tr '[:upper:]' '[:lower:]')

  # If the user input is not empty and does not match the default value, then validate the input
  if [[ ${#tmp} -gt 0 ]] && [[ "$tmp" != "$default_value" ]]; then

    if [[ "$tmp" == '1' ]] || [[ "$tmp" == 'yes' ]] || [[ "$tmp" == 'y' ]] || [[ "$tmp" == 't' ]] || [[ "$tmp" == 'true' ]] ||
      [[ "$tmp" == 'true' ]]; then
      tmp='1'
    elif [[ "$tmp" == '2' ]] || [[ "$tmp" == 'no' ]] || [[ "$tmp" == 'n' ]] || [[ "$tmp" == 'f' ]] || [[ "$tmp" == 'false' ]] || [[ "$tmp" == '0' ]] ||
      [[ "$tmp" == 'false' ]]; then
      tmp='0'
    else
      echo ""
      echo "Invalid selection: $tmp"
      echo ""
      return 1
    fi

    # shellcheck disable=SC2034
    YNAR="$tmp"
  fi

  echo ""

  return 0
}

get_environment_type() {
  echo "What type of environment is this?"
  echo "  1) Production"
  echo "  2) Development"
  echo ""
  echo "Enter your selection and then press return ['$PDA_ENV_TYPE']:"
  read -r tmp
  tmp=$(echo "$tmp" | xargs)
  tmp=$(echo "$tmp" | tr '[:upper:]' '[:lower:]')

  if [[ ${#tmp} -gt 0 ]] && [[ "$tmp" != "$PDA_ENV_TYPE" ]]; then

    if [[ "$tmp" == '1' ]] || [[ "$tmp" == 'prod' ]]; then
      tmp='production'
    elif [[ "$tmp" == '2' ]] || [[ "$tmp" == 'dev' ]]; then
      tmp='development'
    else
      echo ""
      echo "Invalid selection: $tmp"
      echo ""
      return 1
    fi

    # shellcheck disable=SC2034
    PDA_ENV_TYPE="$tmp"
  fi

  echo ""

  return 0
}

get_db_engine() {
  echo "Which database engine will you be using?"
  echo "  1) MySQL"
  echo "  2) PostgreSQL"
  echo "  3) SQLite"
  echo ""
  echo "Enter your selection and then press return ['$PDA_DB_ENGINE']:"
  read -r tmp
  tmp=$(echo "$tmp" | xargs)
  tmp=$(echo "$tmp" | tr '[:upper:]' '[:lower:]')

  if [[ ${#tmp} -gt 0 ]] && [[ "$tmp" != "$PDA_DB_ENGINE" ]]; then

    if [[ "$tmp" == '1' ]] || [[ "$tmp" == 'mysql' ]]; then
      tmp='mysql'
    elif [[ "$tmp" == '2' ]] || [[ "$tmp" == 'pgsql' ]] || [[ "$tmp" == 'postgresql' ]]; then
      tmp='postgres'
    elif [[ "$tmp" == '3' ]] || [[ "$tmp" == 'sqlite3' ]]; then
      tmp='sqlite'
    else
      echo ""
      echo "Invalid selection: $tmp"
      echo ""
      return 1
    fi

    # shellcheck disable=SC2034
    PDA_DB_ENGINE="$tmp"
  fi

  echo ""

  return 0
}

get_server_type() {
  echo "What type of HTTP server would you like to use to run the application?"
  echo "  1) Gunicorn"
  echo "  2) Uvicorn"
  echo "  3) UWSGI"
  echo "  4) Django Development Server"
  echo ""
  echo "Typically, Django's development server should only be used for development purposes."
  echo ""
  echo "Enter your selection and then press return ['$PDA_SERVER_TYPE']:"
  read -r tmp
  tmp=$(echo "$tmp" | xargs)
  tmp=$(echo "$tmp" | tr '[:upper:]' '[:lower:]')

  if [[ ${#tmp} -gt 0 ]] && [[ "$tmp" != "$PDA_SERVER_TYPE" ]]; then

    if [[ "$tmp" == '1' ]] || [[ "$tmp" == 'gcorn' ]] || [[ "$tmp" == 'g' ]] || [[ "$tmp" == 'gun' ]]; then
      tmp='gunicorn'
    elif [[ "$tmp" == '2' ]] || [[ "$tmp" == 'ucorn' ]] || [[ "$tmp" == 'u' ]] || [[ "$tmp" == 'uvi' ]]; then
      tmp='uvicorn'
    elif [[ "$tmp" == '3' ]] || [[ "$tmp" == 'uwsgi' ]] || [[ "$tmp" == 'uw' ]] || [[ "$tmp" == 'uws' ]]; then
      tmp='uwsgi'
    elif [[ "$tmp" == '4' ]] || [[ "$tmp" == 'django' ]] || [[ "$tmp" == 'd' ]] || [[ "$tmp" == 'dj' ]]; then
      tmp='django'
    else
      echo ""
      echo "Invalid selection: $tmp"
      echo ""
      return 1
    fi

    # shellcheck disable=SC2034
    PDA_SERVER_TYPE="$tmp"
  fi

  echo ""

  return 0
}

get_venv_path() {
  echo "Where should the virtual environment be located?"
  echo ""
  echo "You may provide an absolute path or a relative path to the project root directory."
  echo ""
  echo "Enter the path where the virtual environment should be created and then press return ['$PDA_VENV_PATH']:"
  read -r tmp
  tmp=$(echo "$tmp" | xargs)

  if [[ ${#tmp} -gt 0 ]] && [[ "$tmp" != "$PDA_VENV_PATH" ]]; then
    # shellcheck disable=SC2034
    PDA_VENV_PATH="$tmp"
  fi

  echo ""

  return 0
}

# Configure the environment type
get_environment_type
input_status=$?
while ! [[ "$input_status" -eq 0 ]]; do
  get_environment_type
  input_status=$?
done

# Update defaults based on chosen environment type while respecting user overrides
if [[ "$PDA_ENV_TYPE" == 'development' ]]; then
  # Update the default to disable automatic startup setup for development environments
  if [[ "$PDACLI_AUTOSTART" == "$PDACLI_AUTOSTART_DEF" ]]; then
    PDACLI_AUTOSTART='0'
  fi

  # Update the default database engine to SQLite for development environments
  if [[ "$PDA_DB_ENGINE" == "$PDACLI_DB_ENGINE_DEF" ]]; then
    PDA_DB_ENGINE='sqlite'
  fi

  # Update the default HTTP server to Django's development server for development environments
  if [[ "$PDA_SERVER_TYPE" == "$PDACLI_SERVER_TYPE_DEF" ]]; then
    PDA_SERVER_TYPE='django'
  fi

  # Update the default to enable virtual environments
  if [[ "$PDA_VENV_ENABLED" == "$PDA_VENV_ENABLED" ]]; then
    PDA_VENV_ENABLED='1'
  fi
fi

# Configure whether or not to automatically run the application on system startup
option_prompt="Would you like to configure the application to automatically run on system startup?"
option_explanation="Depending on your operating system, an appropriate SysVinit script or systemd service file will be created."
get_yes_no_answer "$PDACLI_AUTOSTART" "$option_prompt" "$option_explanation"
input_status=$?
while ! [[ "$input_status" -eq 0 ]]; do
  get_yes_no_answer "$PDACLI_AUTOSTART" "$option_prompt" "$option_explanation"
  input_status=$?
done
PDACLI_AUTOSTART="$YNAR"

# Configure what database engine to use
get_db_engine
input_status=$?
while ! [[ "$input_status" -eq 0 ]]; do
  get_db_engine
  input_status=$?
done

# Configure what HTTP server to use
get_server_type
input_status=$?
while ! [[ "$input_status" -eq 0 ]]; do
  get_server_type
  input_status=$?
done

# Configure whether to use a virtual environment
option_prompt="Would you like to use a Python virtual environment (venv) for this application?"
option_explanation="Typically, a virtual environment should be used for development environments or production " \
  "environments that will run multiple versions of the application."
get_yes_no_answer "$PDA_VENV_ENABLED" "$option_prompt" "$option_explanation"
input_status=$?
while ! [[ "$input_status" -eq 0 ]]; do
  get_yes_no_answer "$PDA_VENV_ENABLED" "$option_prompt" "$option_explanation"
  input_status=$?
done
PDA_VENV_ENABLED="$YNAR"

# Configure the virtual environment path if virtual environment is enabled
if [[ "$PDA_VENV_ENABLED" == "1" ]]; then
  get_venv_path
  input_status=$?
  while ! [[ "$input_status" -eq 0 ]]; do
    get_venv_path
    input_status=$?
  done
fi

# Display the environment configuration
display_configuration
