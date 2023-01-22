# MenuApp
## Stack
- Fastapi
- Sqlmodel(Sqlalchemy)
- Postgresql
- Docker
- Pytest
## Project Setup     
__reminder__: don't forger to configure your interpreter and activate venv.   
- activate venv    
- pip install docker    
- docker compose --env-file .env.dev up -d --build
## Task summary    
FastAPI app with PostgresSQL as db.    
At this moment implemented:     
- 3 models (menu, submenu, dishes) and their ralations     
- CRUD endpoints for them     
- Pytest CRUD tests.     
Tests are in a separate container, running by docker-compose command    


