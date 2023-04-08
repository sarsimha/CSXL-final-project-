# from typing import Annotated
from fastapi import APIRouter, Depends #, Form
from ..services import EventService
from ..models import Event, CreateEvent

api = APIRouter(prefix="/api/event")


# View all events in database
@api.get("", response_model=list[Event], tags=['Event'])
def get_events(eventService: EventService = Depends()) -> list[Event]:
    return eventService.all()

# Create new event
@api.post("/create", response_model=Event, tags=['Event'])
async def create_event(
    create: CreateEvent,
    eventService: EventService = Depends()
):
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
    newEvent = eventService.create_event(newEvent)
    return newEvent