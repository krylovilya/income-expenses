FROM python:3.9.4-slim

RUN apt-get update && apt-get install -y git libpq-dev postgresql-client && pip install poetry && poetry config virtualenvs.create false
WORKDIR /server

COPY ./server/pyproject.toml /server/
COPY ./server/poetry.lock /server/

ARG DEBUG
RUN if [ $DEBUG = "True" ]; \
    then poetry install; \
    else poetry install --no-dev; \
    fi;

COPY ./server /server
