########################################
########### PDA Web UI Image ###########
########################################
FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies via APT
RUN apt update \
    && apt install -y build-essential pkg-config curl nginx \
    && rm -f /etc/nginx/sites-enabled/default

# Install NodeJS
RUN curl -fsSL https://deb.nodesource.com/setup_25.x | bash - \
    && apt install -y nodejs

# Install NPM dependencies
RUN npm -g install vite@7.1.11

# Copy entrypoint script into image
COPY ./deploy/docker/scripts/entrypoint-web.sh /srv/scripts/entrypoint.sh

RUN chmod +x /srv/scripts/*

# Change the working path of the execution context
WORKDIR /srv/app

# Copy the UI source files into the container
COPY ./src-ui .

ENTRYPOINT [ "/srv/scripts/entrypoint.sh" ]

EXPOSE 8000
