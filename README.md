## Run production compose

To quickly run a production docker-compose follow these steps:

1. Create an `.env` file at the project root with the following content:

```sh
AUTH_SECRET_KEY=some_test_secret_key
```

See [`.env.example`](https://github.com/Quatters/platform-for-online-internships/blob/main/.env.example)
for another environment variables which may be used.

2. Run compose:

```sh
docker-compose up --build
```

**Important**: compose must be started as root user. Also, make sure 80 and 8080
ports are free.

3. Create users:

If this is your first run, you should create at least admin user, who can
manage content in platform and create other users. Use following commands:

```sh
docker exec -it backend bash
cd /app
# create admin
python create_user.py --email admin@admin.admin --password admin --role admin
# create intern and teacher (also you can create them as admin using the app itself)
python create_user.py --email intern@intern.intern --password intern --role intern
python create_user.py --email teacher@teacher.teacher --password teacher --role teacher
exit
```

4. Check app at http://internships.localhost.

## Contribute

Every environment variable described below can either be set directly:

```sh
# unix
export ENV_KEY=ENV_VALUE
# windows
set ENV_KEY=ENV_VALUE
```

or by using `.env` file. Look for the [`.env.example`](https://github.com/Quatters/platform-for-online-internships/blob/main/.env.example) to see which are needed or
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
python -m backend
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

### Testing

Run `flake8` linter with

```sh
flake8
# or
python -m flake8
```

Run tests with

```sh
pytest
# or
python -m pytest
```

`pytest` is smart enough to discover test modules (classes, functions) by their
names prefixed with `test_`. Refer to
[`pytest` documentation](https://docs.pytest.org/en/7.3.x/contents.html)
to learn more.

Use `--cov` argument to show coverage report:

```sh
pytest --cov
```

---

**NOTE**

Tests use database specified by `DATABASE_URL` env suffixed with `_test`. E.g.

```sh
# if your env specifies
DATABASE_URL="postgresql://postgres:postgres@localhost/my_db"
# then tests will use
"postgresql://postgres:postgres@localhost/my_db_test"
```

If database does not exist it will be created automatically, migrations will
be applied and test users will be created. Each unit test runs in a
transaction which is rolled back after it ends, so you are free to do
everything is needed. At the end of test session database will be dropped.

---

#### create_user.py

You can use `create_user.py` CLI tool to quickly create user with any role.
User will be saved to database with hashed password as it was a real
registration.

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

Before submitting a pull request, make sure there are no eslint errors:

```sh
yarn lint
```

and app builds successfully:

```sh
yarn build
```
