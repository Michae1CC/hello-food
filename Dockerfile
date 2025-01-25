# syntax=docker/dockerfile:1

FROM python:3.13-slim

COPY ./setup.py ./setup.cfg ./
COPY ./hello_food ./

RUN : \
    pip install flask \
    pip install sqlalchemy \
    echo test

ARG POSTGRES_HOSTNAME="localhost"
ENV POSTGRES_HOSTNAME=${POSTGRES_HOSTNAME}
ENV PYTEST_VERSION=""
ENV CI=""
ENV PROD=""

EXPOSE 5000
ENTRYPOINT [ "pip", "list" ]
