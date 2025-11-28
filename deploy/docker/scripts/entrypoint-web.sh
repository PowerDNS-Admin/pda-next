#!/usr/bin/env bash

npm install

if [ "${PDA_ENV}" == "local" ]; then
  vite --host 0.0.0.0 --port 8000
else
  npm run build
  nginx -g "daemon off;"
fi