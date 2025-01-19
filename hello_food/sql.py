from sqlalchemy import create_engine, Engine, MetaData
from sqlalchemy.pool import StaticPool

from .environ import CI, PYTEST_VERSION, PROD

# engine = create_engine(
#     "sqlite+pysqlite:///:memory:",
#     echo=True,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool,
# )


def get_sa_engine() -> Engine:

    if CI:
        return create_engine(
            "postgresql://webapp:webapp@localhost:5432/webapp", echo=True
        )

    return create_engine(
        "postgresql://webapp:webapp@randi1-5.local:5432/webapp", echo=True
    )


engine: Engine = get_sa_engine()


def get_sa_metadata() -> MetaData:

    if PYTEST_VERSION:
        return MetaData(schema="test")

    return MetaData()


metadata: MetaData = get_sa_metadata()
