from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, ForeignKey, Table

Base = declarative_base()


class Pin(Base):
    __tablename__ = "pin"

    id = Column(String, primary_key=True)
    img_link = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)


class Tag(Base):
    __tablename__ = "tag"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


association_table = Table(
    "association",
    Base.metadata,
    Column("id", primary_key=True),
    Column("pin_id", ForeignKey("pin.id")),
    Column("tag_id", ForeignKey("tag.ig"))
)
