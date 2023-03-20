#!/usr/bin/env bash

PDA_DB_ENGINE='sqlite'
PDA_ENV_TYPE='production'
PDA_SERVER_TYPE=${PDA_SERVER_TYPE:-'gunicorn'}
PDA_VENV_ENABLED=${PDA_VENV_ENABLED:-0}
PDA_VENV_PATH=${PDA_VENV_PATH:-'venv'}

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

get_venv_enabled() {
  PDA_VENV_ENABLED_LABEL='No'
  if [[ "$PDA_VENV_ENABLED" == "1" ]]; then
    PDA_VENV_ENABLED_LABEL='Yes'
  fi

  echo "Would you like to use a Python virtual environment (venv) for this application?"
  echo "  1) Yes"
  echo "  2) No"
  echo ""
  echo "Typically, a virtual environment should be used for development environments or production environments " \
    "that will run multiple versions of the application."
  echo ""
  echo "Enter your selection and then press return ['$PDA_VENV_ENABLED_LABEL']:"
  read -r tmp
  tmp=$(echo "$tmp" | xargs)
  tmp=$(echo "$tmp" | tr '[:upper:]' '[:lower:]')

  if [[ ${#tmp} -gt 0 ]] && [[ "$tmp" != "$PDA_VENV_ENABLED" ]]; then

    if [[ "$tmp" == '1' ]] || [[ "$tmp" == 'yes' ]] || [[ "$tmp" == 'y' ]] || [[ "$tmp" == 't' ]] ||
      [[ "$tmp" == 'true' ]]; then
      tmp='1'
    elif [[ "$tmp" == '2' ]] || [[ "$tmp" == 'no' ]] || [[ "$tmp" == 'n' ]] || [[ "$tmp" == 'f' ]] ||
      [[ "$tmp" == 'false' ]]; then
      tmp='0'
    else
      echo ""
      echo "Invalid selection: $tmp"
      echo ""
      return 1
    fi

    # shellcheck disable=SC2034
    PDA_VENV_ENABLED="$tmp"
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
get_venv_enabled
input_status=$?
while ! [[ "$input_status" -eq 0 ]]; do
  get_venv_enabled
  input_status=$?
done

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
PDA_VENV_ENABLED_LABEL='No'
if [[ "$PDA_VENV_ENABLED" == "1" ]]; then
  PDA_VENV_ENABLED_LABEL='Yes'
fi

echo "Environment Configuration:"
echo "  - Environment Type: $PDA_ENV_TYPE"
echo "  - Database Engine: $PDA_DB_ENGINE"
echo "  - Server Type: $PDA_SERVER_TYPE"
echo "  - Virtual Environment Enabled: $PDA_VENV_ENABLED_LABEL"
if [[ "$PDA_VENV_ENABLED" == "1" ]]; then
  echo "  - Virtual Environment Path: $PDA_VENV_PATH"
fi
echo ""
