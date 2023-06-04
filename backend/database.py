from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import create_database, database_exists
from backend.settings import DATABASE_URL, DEBUG


connect_args = {'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {}

engine_kwargs = {}
if DEBUG:
    engine_kwargs['echo'] = True

engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)

if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
