#!/usr/bin/env bash

PDA_ENV_TYPE='production'
PDA_DB_ENGINE='sqlite'

get_environment_type () {
  echo "What type of environment is this?"
  echo "  1) Production"
  echo "  2) Development"
  echo ""
  echo "Enter your selection and then press return ['$PDA_ENV_TYPE']:"
  read -r tmp
  tmp=$(echo "$tmp" | xargs)
  tmp=$(echo "$tmp" | tr '[:upper:]' '[:lower:]')

  if [[ ${#tmp} -gt 0 ]] && [[ "$tmp" != "$PDA_CONFIG_PATH" ]]; then

    if [[ "$tmp" == '1' ]] || [[ "$tmp" == 'prod' ]]; then
      tmp='production'
    elif [[ "$tmp" == '2' ]] || [[ "$tmp" == 'dev' ]]; then
      tmp='development'
    fi

    # shellcheck disable=SC2034
    PDA_ENV_TYPE="$tmp"
  fi

  echo ""
}

get_db_engine () {
  echo "Which database engine will you be using?"
  echo "  1) MySQL"
  echo "  2) PostgreSQL"
  echo "  3) SQLite"
  echo ""
  echo "Enter your selection and then press return ['$PDA_DB_ENGINE']:"
  read -r tmp
  tmp=$(echo "$tmp" | xargs)
  tmp=$(echo "$tmp" | tr '[:upper:]' '[:lower:]')

  if [[ ${#tmp} -gt 0 ]] && [[ "$tmp" != "$PDA_CONFIG_PATH" ]]; then

    if [[ "$tmp" == '1' ]] || [[ "$tmp" == 'mysql' ]]; then
      tmp='mysql'
    elif [[ "$tmp" == '2' ]] || [[ "$tmp" == 'pgsql' ]] || [[ "$tmp" == 'postgresql' ]]; then
      tmp='postgres'
    elif [[ "$tmp" == '3' ]] || [[ "$tmp" == 'sqlite3' ]]; then
      tmp='sqlite'
    fi

    # shellcheck disable=SC2034
    PDA_DB_ENGINE="$tmp"
  fi

  echo ""
}

# Collect inputs from the user
get_environment_type
get_db_engine

echo "Environment Configuration:"
echo "  - Environment Type: $PDA_ENV_TYPE"
echo "  - Database Engine: $PDA_DB_ENGINE"
echo ""
