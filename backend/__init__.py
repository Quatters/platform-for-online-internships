from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from backend.settings import STATIC_DIR, CLIENT_DOMAIN
from backend.api.routes import routers
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import add_pagination

app = FastAPI()


@app.exception_handler(IntegrityError)
async def unique_violation_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({
            'code': 'integrity_error',
            'original_message': str(exc),
        })
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_DOMAIN],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=['*'],
)

add_pagination(app)

for router in routers:
    app.include_router(router, prefix='/api')

app.mount(
    '/static',
    StaticFiles(directory=STATIC_DIR),
    name='static',
)
