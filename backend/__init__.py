from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse
from backend.settings import STATIC_DIR, CLIENT_DOMAIN
from backend.api.routes import routers
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

app = FastAPI()


@app.exception_handler(IntegrityError)
async def unique_violation_exception_handler(request: Request, exc: IntegrityError):
    if isinstance(exc.orig, UniqueViolation):
        return PlainTextResponse(f"Error: {exc._message()}", status_code=400)
    raise exc

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
