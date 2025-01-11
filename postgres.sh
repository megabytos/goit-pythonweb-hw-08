#!/bin/bash

# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs)

docker run --name Postgres-hw08 \
  -p 5432:5432 \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e POSTGRES_DB=$POSTGRES_DB \
  -d postgres