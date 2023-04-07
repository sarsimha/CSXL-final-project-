from fastapi import APIRouter, Depends
from ..services import EventService
from ..models import Event


api = APIRouter(prefix="/api/event")
@api.get("", response_model=list[Event], tags=['Event'])
def get_events(eventService: EventService = Depends()) -> list[Event]:
    return eventService.all()
