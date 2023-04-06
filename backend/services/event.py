from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Event
from ..entities import EventEntity

class EventService:
    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    # Pull data from event database
    def all(self) -> list[Event] | None:
        query = select(EventEntity)
        event_entities: list[EventEntity] = self._session.scalars(query).all()
        if event_entities is None:
            return None
        else:
            return [entity.to_model() for entity in event_entities]