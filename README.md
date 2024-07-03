# MenuApp
## Stack
- Fastapi
- Sqlmodel(Sqlalchemy)
- Postgresql
- Docker
- Pytest
- Redis
- Celery
- Rabbitmq (as broker and backend for celery)
- pre-commit (linters)

## Project Setup
__reminder__: don't forget to configure your interpreter and activate venv.
- activate venv
- pip install docker
- docker compose -f docker-compose.yml --env-file .env.dev up -d --build
- docker compose -f docker-compose.tests.yml --env-file .env.tests up -d --build
## Task summary
FastAPI app with PostgresSQL as db. It's fully async (tests, endpoints, db, cache).
Simple crud operations, some data aggregations.
At this moment implemented:
- 3 models (menu, submenu, dishes) and their relations
- CRUD endpoints for them
- Pytest CRUD tests.
- Caching get requests for models(detail/list views)
- Celery task: conversion data from db to excel file. (file response)

Tests are in a separate container, running by docker-compose command.
