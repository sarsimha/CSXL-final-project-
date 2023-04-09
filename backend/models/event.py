"""Event is the data object that is connected to organizations in the CS dept."""
# from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Event(BaseModel):
    id: int | None
    name: str
    orgName: str
    location: str
    description: str
    date: str
    time: str
    # orgId: Optional[int]

class CreateEvent(BaseModel):
    # id: int | None
    name: str
    orgName: str
    location: str
    description: str
    date: str
    time: str