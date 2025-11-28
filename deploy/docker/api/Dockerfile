########################################
############ PDA API Image #############
########################################
FROM python:3.12

WORKDIR /srv/app

# Copy the Python source files into the container
COPY ./src-api ./src

# Copy the Python pip requuirements into the container
COPY ./requirements.txt ./requirements.txt

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir -r requirements.txt
