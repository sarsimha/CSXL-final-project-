"""Organization is the data object of a student organization that is registered in the CS dept."""

from pydantic import BaseModel

class Organization(BaseModel):
    id: int | None = None
    name: str
    description: str
    # TODO: Add events: list[Events] and create Event model