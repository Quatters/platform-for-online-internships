#!/bin/sh

alembic upgrade head
gunicorn backend:app --worker-class uvicorn.workers.UvicornWorker
