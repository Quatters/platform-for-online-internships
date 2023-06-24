import uvicorn
from backend.settings import UVICORN_CONFIG


uvicorn.run(**UVICORN_CONFIG)
