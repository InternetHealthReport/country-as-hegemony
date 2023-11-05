# syntax=docker/dockerfile:1

###############################################################################
# Documentation
#
# Component: Country AS Hegemony
#
# Usage:
#   - docker run --rm --name country_as_hegemony \
#       -e KAFKA_HOST="kafka1:9092" \
#       internethealthreport/country_as_hegemony
#   
# Note:
#   - You have to pass set environment variable KAFKA_HOST (eg. `--env KAFKA_HOST="kafka:9092") 
#   - Config files are already included in the container.

ARG IMAGE_VERSION="ihr"
ARG PYTHON_VERSION="3.6"

FROM internethealthreport/python:${PYTHON_VERSION}-${IMAGE_VERSION}


# Switch to root install dependencies
USER root

SHELL ["/bin/bash", "-c"]

COPY ./requirements.txt .

# Install wget (needed by the run.sh script)
RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install wget -y --no-install-recommends \
    && pip install -r requirements.txt \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to ihr user to run rootless
USER ihr:ihr

COPY . .
COPY --chown=ihr:ihr --chmod=777 ./run.sh .

ENTRYPOINT /app/run.sh