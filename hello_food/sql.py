from sqlalchemy import create_engine, MetaData
from sqlalchemy.pool import StaticPool

# engine = create_engine(
#     "sqlite+pysqlite:///:memory:",
#     echo=True,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool,
# )

engine = create_engine(
    "postgresql://webapp:webapp@randi1-5.local:5432/webapp", echo=True
)

metadata = MetaData(schema="test")
