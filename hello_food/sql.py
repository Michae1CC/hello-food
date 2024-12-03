from sqlalchemy import create_engine, MetaData
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    echo=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

metadata = MetaData()
