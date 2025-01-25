from sqlalchemy import create_engine, Engine, MetaData
from sqlalchemy.pool import StaticPool

from .environ import CI, PYTEST_VERSION, POSTGRES_HOSTNAME, PROD

engine: Engine = create_engine(
    f"postgresql://webapp:webapp@{POSTGRES_HOSTNAME}:5432/webapp", echo=True
)


def get_sa_metadata() -> MetaData:

    if CI:
        return MetaData()

    elif PYTEST_VERSION:
        return MetaData(schema="test")

    return MetaData()


metadata: MetaData = get_sa_metadata()
