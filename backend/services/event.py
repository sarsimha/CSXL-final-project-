from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Event, User
from ..entities import EventEntity
from .permission import PermissionService

class EventService:
    _session: Session

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    # Pull all events that exists in the event database
    def all(self) -> list[Event] | None:
        query = select(EventEntity)
        event_entities: list[EventEntity] = self._session.scalars(query).all()
        if event_entities is None:
            return None
        else:
            return [entity.to_model() for entity in event_entities]
        
    # Create new event
    def create_event(self, subject: User, event: Event) -> Event:
        #TODO: Add check for permissions (permission to access page + permission to submit)
        self._permission.enforce(subject, 'event.create_event', 'event/create/')

        entity = EventEntity.from_model(event)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()