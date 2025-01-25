# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN : \
    && python -m pip install flask \
    && python -m pip install sqlalchemy \
    && python -m pip install psycopg2-binary \
    && python -m pip install boto3

ARG POSTGRES_HOSTNAME
ENV POSTGRES_HOSTNAME=${POSTGRES_HOSTNAME}
ENV AWS_DEFAULT_REGION="us-east-1"

# Copy the source code into the container.
COPY ./setup.py ./setup.cfg ./
COPY ./hello_food ./

# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
CMD python3 -m flask run --port 8080 --host=0.0.0.0
