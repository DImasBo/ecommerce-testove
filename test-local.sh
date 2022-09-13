#! /usr/bin/env bash

# Exit in case of error
set -e

export DOMAIN=localhost

docker-compose build backend db
docker-compose up -d backend db
docker-compose run --rm backend pytest
