"""Event is the data object that is connected to organizations in the CS dept."""
from datetime import datetime
from pydantic import BaseModel


class Event(BaseModel):
    id: int | None
    name: str
    orgName: str
    location: str
    description: str
    date: datetime

