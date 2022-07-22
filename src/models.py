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


class PinTag(Base):
    __tablename__ = "pin_tag"

    id = Column(String)
    pin_id = Column(ForeignKey("pin.id"), primary_key=True)
    tag_id = Column(ForeignKey("tag.id"), primary_key=True)
