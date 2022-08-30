from contextlib import contextmanager
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker, Session
from models import Pin, Tag, PinTag
from typing import Iterable
from schemas import ReqModel

DATABASE_URL = "postgresql://postgres:610700@localhost/pin"


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self._engine))

    @contextmanager
    def session(self):
        session: Session = self._session_factory()
        try:
            yield session
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def create(self, item: ReqModel) -> Iterable[Pin]:
        with self._session_factory() as session:
            pin_to_add = Pin(img_link=item.img_link,
                             title=item.title,
                             description=item.description)

            tag_to_add = Tag(name=item.tags)
            session.add(tag_to_add)
            session.add(pin_to_add)
            session.flush()

            pin_tag_to_add = PinTag(pin_id=pin_to_add.id,
                                    tag_id=tag_to_add.id)
            session.add(pin_tag_to_add)
            session.commit()

            session.refresh(pin_to_add)
            session.refresh(tag_to_add)
            session.refresh(pin_tag_to_add)
            return pin_to_add

    def get_all(self) -> Iterable[Pin]:
        with self._session_factory() as session:
            return session.query(Pin).all()

    def delete(self, item_id: int) -> None:
        with self._session_factory() as session:
            pin_to_delete = Database.__find_pin(item_id, session)
            session.delete(pin_to_delete)
            tags = Database.__find_tags(item_id, session)
            session.delete(tags)
            session.commit()

    def update(self, item_id: int, item: ReqModel) -> Iterable[Pin]:
        with self._session_factory() as session:
            props = dict(item)
            pin_to_update = Database.__find_pin(item_id, session)
            for key, value in props.items():
                if key == "tags":
                    tags = Database.__find_tags(item_id, session)
                    setattr(tags, "name", value)
                setattr(pin_to_update, key, value)
            session.commit()
            session.refresh(pin_to_update)
            return pin_to_update

    @staticmethod
    def __find_pin(item_id, session):
        entity: Pin = session.query(Pin).filter(Pin.id == item_id).first()
        if not entity:
            raise PinNotFoundError(item_id)
        return entity

    @staticmethod
    def __find_tags(pin_id, session):
        pin_tag_entity: PinTag = session.query(PinTag).filter(PinTag.pin_id == pin_id).first()
        if not pin_tag_entity:
            raise PinTagNotFoundError(pin_id)
        tag_entity: Tag = session.query(Tag).filter(Tag.id == pin_tag_entity.tag_id).first()
        if not tag_entity:
            raise TagNotFoundError(pin_tag_entity.tag_id)
        return tag_entity


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id: int):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class PinNotFoundError(NotFoundError):
    entity_name = "Pin"


class PinTagNotFoundError(NotFoundError):
    entity_name = "PinTag"


class TagNotFoundError(NotFoundError):
    entity_name = "Tag"
