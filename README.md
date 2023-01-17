# MenuApp
## Stack
- Fastapi
- Postgresql
- Docker
## Project Setup     
reminder: don't forger to configure your interpreter and activate venv.   
- activate venv    
- pip install docker    
- docker compose --env-file .env.dev up -d --build
- docker-compose exec menu_app alembic upgrade head   
## Task summary    
FastAPI app with PostgresSQL as db.
todo: finish documentation
