"""Event Service.

The Event Service provides access to the Event model and its associated database operations such as creating an event
and viewing all events.
"""


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

    def all(self) -> list[Event] | None:
        """List Events from database.

        Returns:
            list[Event] | None: The list of events or None if not found."""
        query = select(EventEntity)
        event_entities: list[EventEntity] = self._session.scalars(query).all()
        if event_entities is None:
            return None
        else:
            return [entity.to_model() for entity in event_entities]
        
    def create_event(self, subject: User | None, event: Event) -> Event:
        """Create new event.

        The subject must have the 'event.create_event' permission on the 'event/create/' resource.

        Args:
            subject: The user performing the action (or None for just pytest).
            event: The event to create from api.

        Returns:
            Event: The created event from the database.

        Raises:
            PermissionError: If the subject does not have the required permission."""
        if subject:
            self._permission.enforce(subject, 'event.create_event', 'event/create/')
        entity = EventEntity.from_model(event)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()
    
    def delete_event(self, subject: User | None, eventId: int) -> bool:
        """Delete event.

        The subject must have the 'event.delete_event' permission on the 'event/delete/{eventId}' resource.

        Args:
            subject: The user performing the action (or None for just pytest).
            eventId: The id of event to delete from api.

        Returns:
            bool: True if function completes.

        Raises:
            PermissionError: If the subject does not have the required permission."""
        if subject:
            self._permission.enforce(subject, 'event.delete_event', f'event/delete/{eventId}')
        entity = self._session.get(EventEntity, eventId)
        self._session.delete(entity)
        self._session.commit()
        return True
    
    def get_event(self, subject:User, id: int) -> Event | None:
        """Get event.

        The subject must have the 'event.get_event' permission on the 'event/get/{eventId}' resource.

        Args:
            subject: The user performing the action (or None for just pytest).
            eventId: The id of event to get from api.

        Returns:
            Event: The event fetched from the database.

        Raises:
            PermissionError: If the subject does not have the required permission.
            404Error: If the event does not exist. """
        if subject:
            self._permission.enforce(subject, 'event.get_event', 'event/get/{id}/')

        query = select(EventEntity).where(EventEntity.id == id)
        event_entity: EventEntity = self._session.scalar(query)
        if event_entity is None:
            return None
        else:
            model = event_entity.to_model()
            return model

    def update_event(self, subject:User, event: Event) -> Event:
        """Update event.

        The subject must have the 'event.update_event' permission on the 'event/update/{eventId}' resource.

        Args:
            subject: The user performing the action (or None for just pytest).
            eventId: The id of event to update event from api.

        Returns:
            Event: The updated event from the database.

        Raises:
            PermissionError: If the subject does not have the required permission.
            404Error: If the event does not exist. """
            
        if subject:
            self._permission.enforce(subject, 'event.update_event', 'event/update/{id}/')

        entity = self._session.get(EventEntity, event.id)
        entity.update(event)
        self._session.commit()
        return entity.to_model() 