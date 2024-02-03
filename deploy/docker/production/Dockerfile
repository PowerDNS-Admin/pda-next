FROM python:3.10-slim-bullseye
ARG PACKAGES
ENV PACKAGES=${PACKAGES:-"build-essential,python3-dev,python3-pip,python3-venv,npm"}
RUN apt-get update && apt-get install -y $(echo "$PACKAGES" | tr ',' ' ')
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /srv
COPY --chown=1000:1000 . /srv/
RUN pip install .
RUN cd src/static && npm install
USER 1000:1000