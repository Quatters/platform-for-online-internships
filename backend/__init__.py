from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.settings import STATIC_DIR, CLIENT_DOMAIN
from backend.api.routes import routers


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_DOMAIN],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=['*'],
)

for router in routers:
    app.include_router(router, prefix='/api')

app.mount(
    '/static',
    StaticFiles(directory=STATIC_DIR),
    name='static',
)
