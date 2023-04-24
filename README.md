## Contribute

Every environment variable described below can either be set directly:

```sh
# unix
export ENV_KEY=ENV_VALUE
# windows
set ENV_KEY=ENV_VALUE
```

or using `.env` file. Look for the `.env.example` to see which are needed or
may be set.

### Backend

We are using Python 3.11 and [FastAPI](https://fastapi.tiangolo.com/).
To start, make virtual env, activate it and install dependencies:

```sh
# all in the root directory
source/to/python3.11 -m venv env
# unix
source env/bin/activate
# windows
.\env\Scripts\activate.bat
pip install -r requirements.txt
```

Before backend can be started it's required to set database by providing
`DATABASE_URL` env variable.

Run development server using

```sh
python -m backend --dev
```

To check generated OpenAPI schema visit `/docs` or `/redoc`.

Migrations are handled by
[Alembic](https://alembic.sqlalchemy.org/en/latest/) package. Example usage:

```sh
# make migration
alembic revision --autogenerate -m '<migration name>'
# check if there are migrations that are not applied
alembic check
# migrate to the latest revision
alembic upgrade head
```

Before opening PR, make sure there are no `flake8` errors:

```sh
python -m flake8
```

### Frontend

Here we are using Nuxt 3. To start, install dependencies:

```sh
# root directory
npm i
```

Up development server:

```sh
npm run dev
```
