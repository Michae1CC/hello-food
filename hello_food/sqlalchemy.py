from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# Create a single global session maker
Session = sessionmaker(engine, autoflush=False)


class Base(DeclarativeBase):
    pass
