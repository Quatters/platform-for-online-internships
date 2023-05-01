## Contribute

Every environment variable described below can either be set directly:

```sh
# unix
export ENV_KEY=ENV_VALUE
# windows
set ENV_KEY=ENV_VALUE
```

or by using `.env` file. Look for the `.env.example` to see which are needed or
may be set.

OpenAPI schema plays an important role for both backend and frontend. On backend
you are could use SwaggerUI to quickly test recent endpoints. On frontend schema
translates to typescript types which are used directly in the code.

So don't forget to regenerate schema if there are updates on backend:

```sh
python generate_openapi.py
```

and then regenerate types on frontend:

```sh
# cd frontend
npx openapi-typescript ../openapi.json --output openapi.ts
```

### Backend

We are using Python 3.11 and [FastAPI](https://fastapi.tiangolo.com/).
To start, make virtual env, activate it and install dependencies:

```sh
# all in the root directory
source/to/python3.11 -m venv env
# unix
source env/bin/activate
# windows cmd
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

all tests are passed:

```sh
python -m pytest tests.py
```

#### create_user.py

You can use `create_user.py` CLI tool to quickly create user with any role.
User saves in database with hashed password as it was a real registration.

```sh
# get help
python create_user.py -h
# create admin user
python create_user.py \
    --email admin@admin.admin \
    --password admin \
    --role admin \
    --first-name admin \
    --last-name admin \
    --patronymic admin
```

### Frontend

Here we are using Nuxt 3. To start, install dependencies:

```sh
# cd frontend
yarn
```

Up development server:

```sh
# cd frontend
yarn dev
```
