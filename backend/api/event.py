from fastapi import APIRouter, Depends, HTTPException
from ..services import EventService, UserPermissionError
from ..models import Event, CreateEvent, User, EventForm
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



#Get Event by ID
@api.get("/get/{id}", response_model = Event, tags=['Event'])
def get_event(id:int, subject: User= Depends(registered_user), eventService: EventService = Depends()):
    try:
        event = eventService.get_event(subject, id)
        return event
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@api.put("/update/{id}", response_model = Event, tags=['Event'])
def update_event(id:int, eventForm: EventForm, subject: User= Depends(registered_user), eventService:EventService = Depends()):
    try:
        event = eventService.get_event(subject, id)
        if event is None:
            raise HTTPException(status_code=404, detail=str("Event doesn't exist"))
        event.name = eventForm.name
        event.orgName = eventForm.orgName
        event.location = eventForm.location
        event.description = eventForm.description
        event.date = eventForm.date
        event.time = eventForm.time
        event = eventService.update_event(subject, event)
        return event
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

