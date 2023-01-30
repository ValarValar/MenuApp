import uvicorn
from fastapi import FastAPI

from api.v1.resources.dishes import router as dishes_router
from api.v1.resources.menus import router as menus_router
from api.v1.resources.submenus import router as submenus_router
from core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    docs_url=f'{settings.API_V1_STR}/openapi',
    redoc_url=f'{settings.API_V1_STR}/redoc',
    # Адрес документации в формате OpenAPI
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)


@app.get('/')
def root():
    return {'message': 'Hello World'}


@app.on_event('startup')
def startup_db_client():
    pass


@app.on_event('shutdown')
def shutdown_db_client():
    pass


submenus_router.include_router(
    router=dishes_router, prefix='/{submenu_id}/dishes', tags=['dishes'],
)
menus_router.include_router(
    router=submenus_router,
    prefix='/{menu_id}/submenus',
)
app.include_router(router=menus_router, prefix=f'{settings.API_V1_STR}/menus')

if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
