# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13
FROM --platform=linux/amd64 python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the source code into the container.
COPY ./setup.py ./setup.cfg README.md ./
COPY ./hello_food ./hello_food

RUN : \
    && python -m pip install setuptools \
    && python -m pip install -e '.'

ARG POSTGRES_HOSTNAME
ENV POSTGRES_HOSTNAME=${POSTGRES_HOSTNAME}
ENV AWS_DEFAULT_REGION="us-east-1"
ENV FLASK_APP=./hello_food/app.py

# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
CMD python3 -m flask run --port 8080 --host=0.0.0.0
