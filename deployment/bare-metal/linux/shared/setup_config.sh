#!/usr/bin/env bash

PDA_SECRET_KEY=$(pda gen_salt -r)

touch conf/config.yml

tee .env.test &> /dev/null <<EOF
PDA_ACCOUNT_EMAIL_REQUIRED=1
PDA_ADMIN_EMAIL=youremail@yourdomain.com
PDA_ADMIN_FROM_EMAIL=youremail@yourdomain.com
PDA_ADMIN_NAME=Your Name
PDA_CONFIG_PATH=conf/config.yml
PDA_DB_URL=sqlite:///pda.db
PDA_DEBUG=1
PDA_EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
PDA_LOG_LEVEL_APP=DEBUG
PDA_REDIS_URL=redis://127.0.0.1:6379/0
PDA_SECRET_KEY=$PDA_SECRET_KEY
PDA_SECURE_HSTS_SECONDS=0
PDA_SECURE_SSL_REDIRECT=0
PDA_SITE_EMAIL=admin@powerdnsadmin.org
PDA_SITE_FROM_EMAIL=demo@powerdnsadmin.org
PDA_SITE_LOGO=https://demo.powerdnsadmin.org/static/img/logo.png
PDA_SITE_TITLE=PowerDNS Admin
PDA_SITE_URL=https://demo.powerdnsadmin.org
PDA_TIME_ZONE=America/Indiana/Indianapolis
PDA_USE_HTTPS_IN_ABSOLUTE_URLS=0
EOF
