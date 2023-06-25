FROM python:3.11

WORKDIR /app

COPY alembic.ini alembic.ini
COPY requirements.txt requirements.txt
COPY requirements-prod.txt requirements-prod.txt

RUN pip install --no-cache-dir \
    -r requirements.txt \
    -r requirements-prod.txt

COPY entrypoint.sh entrypoint.sh
COPY create_user.py create_user.py

RUN chmod +x ./entrypoint.sh

COPY ./backend /app/backend

ENTRYPOINT [ "./entrypoint.sh" ]
