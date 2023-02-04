# MenuApp
## Stack
- Fastapi
- Sqlmodel(Sqlalchemy)
- Postgresql
- Docker
- Pytest
- Redis
- pre-commit (linters)
## Project Setup
__reminder__: don't forger to configure your interpreter and activate venv.
- activate venv
- pip install docker
- docker compose -f docker-compose.yml --env-file .env.dev up -d --build
- docker compose -f docker-compose.tests.yml --env-file .env.tests up -d --build
## Task summary
FastAPI app with PostgresSQL as db.
At this moment implemented:
- 3 models (menu, submenu, dishes) and their relations
- CRUD endpoints for them
- Pytest CRUD tests.
Tests are in a separate container, running by docker-compose command.
