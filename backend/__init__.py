from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from backend.settings import STATIC_DIR
from backend.settings import API_VERSION
from backend.api.routers import routers


app = FastAPI()
api_router = APIRouter(prefix=f'/api/{API_VERSION}')

for router in routers:
    api_router.include_router(router)

app.include_router(api_router)

app.mount(
    '/static',
    StaticFiles(directory=STATIC_DIR),
    name='static',
)
