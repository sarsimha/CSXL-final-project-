# from typing import Annotated
from fastapi import APIRouter, Depends #, Form
from ..services import EventService
from ..models import Event, CreateEvent

api = APIRouter(prefix="/api/event")


@api.get("", response_model=list[Event], tags=['Event'])
def get_events(eventService: EventService = Depends()) -> list[Event]:
    return eventService.all()

@api.post("/create", response_model=Event, tags=['Event'])
async def create_event(
    create: CreateEvent,
    eventService: EventService = Depends()
):
    #TODO: check if event already exists or not
    event = Event(
        #TODO: figure out how ID is added or not
        name=create.name,
        orgName=create.orgName,
        location=create.location,
        description=create.description,
        date=create.date,
        time=create.time
    )
    event = eventService.create_event(event)
    return event