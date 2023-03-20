#!/usr/bin/env bash

case "$OSTYPE" in
  solaris*) PDACLI_PLATFORM='solaris' ;;
  darwin*)  PDACLI_PLATFORM='osx' ;;
  linux*)   PDACLI_PLATFORM='linux' ;;
  bsd*)     PDACLI_PLATFORM='bsd' ;;
  msys*)    PDACLI_PLATFORM='windows' ;;
  cygwin*)  PDACLI_PLATFORM='windows' ;;
  *)        PDACLI_PLATFORM='unknown' ;;
esac

if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    PDACLI_OS=$NAME
    PDACLI_VER=$VERSION_ID
elif type lsb_release >/dev/null 2>&1; then
    # linuxbase.org
    PDACLI_OS=$(lsb_release -si)
    PDACLI_VER=$(lsb_release -sr)
elif [ -f /etc/lsb-release ]; then
    # For some versions of Debian/Ubuntu without lsb_release command
    . /etc/lsb-release
    PDACLI_OS=$DISTRIB_ID
    PDACLI_VER=$DISTRIB_RELEASE
elif [ -f /etc/debian_version ]; then
    # Older Debian/Ubuntu/etc.
    PDACLI_OS=Debian
    PDACLI_VER=$(cat /etc/debian_version)
elif [ -f /etc/SuSe-release ]; then
    # Older SuSE/etc.
    PDACLI_OS=SuSE
    PDACLI_VER=$(cat /etc/SuSe-release | sed 's/.*release \([0-9.]*\).*/\1/')
elif [ -f /etc/redhat-release ]; then
    # Older Red Hat, CentOS, etc.
    PDACLI_OS=CentOS
    PDACLI_VER=$(cat /etc/redhat-release | sed 's/.*release \([0-9.]*\).*/\1/')
else
    # Fall back to uname, e.g. "Linux <version>", also works for BSD, etc.
    PDACLI_OS=$(uname -s)
    PDACLI_VER=$(uname -r)
fi

PDACLI_DISTRO=
PDACLI_OS=$(echo "$PDACLI_OS" | tr '[:upper:]' '[:lower:]')
PDACLI_PLATFORM=$(echo "$PDACLI_PLATFORM" | tr '[:upper:]' '[:lower:]')
PDACLI_VER=$(echo "$PDACLI_VER" | tr '[:upper:]' '[:lower:]')

if [[ $PDACLI_PLATFORM == 'bsd' ]]; then
  echo 'BSD is not supported at this time.'

elif [[ $PDACLI_PLATFORM == 'linux' ]]; then

  if [[ $PDACLI_OS == 'debian' ]] || [[ $PDACLI_OS == 'ubuntu' ]] || [[ $PDACLI_OS == 'kubuntu' ]]; then
    PDACLI_DISTRO='debian'
  else
    echo "Unsupported Linux distribution: $PDACLI_OS"
    return 1
  fi

elif [[ $PDACLI_PLATFORM == 'osx' ]]; then
  echo 'OSX is not supported at this time.'

elif [[ $PDACLI_PLATFORM == 'solaris' ]]; then
  echo 'Solaris is not supported at this time.'

elif [[ $PDACLI_PLATFORM == 'windows' ]]; then
  echo 'Windows is not supported at this time.'

else
  echo "Unsupported platform: $PDACLI_PLATFORM"
  return 1
fi

if [[ $PDACLI_DISTRO == '' ]]; then
  echo 'Please use a supported platform.'
  return 1
fi

PDACLI_DISTRO=$(echo "$PDACLI_DISTRO" | tr '[:upper:]' '[:lower:]')
