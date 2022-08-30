from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, ForeignKey, Integer, BigInteger

Base = declarative_base()


class Pin(Base):
    __tablename__ = "pin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    img_link = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class PinTag(Base):
    __tablename__ = "pin_tag"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    pin_id = Column(ForeignKey("pin.id"), autoincrement=False)
    tag_id = Column(ForeignKey("tag.id"), autoincrement=False)
