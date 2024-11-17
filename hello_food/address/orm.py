from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ..sql import Base


class AddressORM(Base):
    __tablename__ = "Address"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    unit: Mapped[str]
    street_name: Mapped[str]
    suburb: Mapped[str]
    postcode: Mapped[int]
