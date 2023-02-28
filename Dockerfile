FROM python:3-alpine

RUN apk add --no-cache libpq postgresql-client \
    alpine-sdk libffi-dev openssl-dev tmux

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && pip install --no-cache-dir psycopg2 \
    && apk del --no-cache .build-deps

RUN pip install \
    python-intercom \
    argparse \
    requests \
    jsonschema \
    slack_sdk \
    intuitlib.client \
    quickbooks 


WORKDIR /scripts
COPY . .