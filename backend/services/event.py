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

    # Pull all events that exists in the event database
    def all(self) -> list[Event] | None:
        query = select(EventEntity)
        event_entities: list[EventEntity] = self._session.scalars(query).all()
        if event_entities is None:
            return None
        else:
            return [entity.to_model() for entity in event_entities]
        
    # Create new event
    def create_event(self, event: Event) -> Event:
        #TODO: Add check for permissions (permission to access page + permission to submit)
        #self._permission.enforce(subject, 'event_create', 'event/create/')

        entity = EventEntity.from_model(event)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()