from fastapi import APIRouter, Depends, HTTPException
from ..services import EventService, UserPermissionError
from ..models import Event, CreateEvent, User
from .authentication import registered_user

api = APIRouter(prefix="/api/event")


# View all events in database
@api.get("", response_model=list[Event], tags=['Event'])
def get_events(eventService: EventService = Depends()) -> list[Event]:
    """Get list of all events."""
    return eventService.all()

# View all events based on organization
@api.get("/{org}", response_model=list[Event], tags=['Event'])
def get_events_org(org: str, eventService: EventService = Depends()) -> list[Event]:
    """Get list of all events based on organization."""
    allEvents = eventService.all()
    eventsOfOrg = []
    for event in allEvents:
        if event.orgName == org:
            eventsOfOrg.append(event)
    return eventsOfOrg

# Create new event
@api.post("/create", response_model=Event, tags=['Event'])
async def create_event(
    create: CreateEvent,
    subject: User = Depends(registered_user),
    eventService: EventService = Depends()
):
    """If registered user has permission, create new event and add to database. If not, raise UserPermissionError."""
    try:
        #TODO: check if event already exists or not
        # Use form data to create new event
        newEvent = Event(
            name=create.name,
            orgName=create.orgName,
            location=create.location,
            description=create.description,
            date=create.date,
            time=create.time
        )
        # Add new event to database
        newEvent = eventService.create_event(subject, newEvent)
        return newEvent
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
# Delete event
@api.delete("/delete/{eventId}", response_model=Event, tags=['Event'])
def delete_event(
    eventId: int,
    subject: User = Depends(registered_user),
    eventService: EventService = Depends()
) -> bool:
    try:
        return eventService.delete_event(subject, eventId)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
