"""Organization is the data object of a student organization that is registered in the CS dept."""

from pydantic import BaseModel

class Organization(BaseModel):
    id: int | None = None
    name: str
    description: str
    # TODO: Add events: list[Events] and create Event model
    # TODO: Figure out how to connect organization and events through ID