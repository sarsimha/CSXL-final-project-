from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .organization_entity import OrganizationEntity
from .entity_base import EntityBase
from ..models import Event

class EventEntity(EntityBase):
    __tablename__ = 'event'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique =True)
    name: Mapped[str] = mapped_column(String(32), index=True)
    description: Mapped[str] = mapped_column(String(128))
    orgName: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    # Date and time were split into two objects so that it would be easier for users to input data during create form.
    # This could potentially be changed back to DateTime depending on what functionality we need.
    date: Mapped[str] = mapped_column(String)
    time: Mapped[str] = mapped_column(String)

    org_id: Mapped[int] = mapped_column(ForeignKey('organization.id'), nullable = True)
    #organization: Mapped[OrganizationEntity] = relationship(back_populates='event')

    @classmethod
    def from_model(cls, model: Event) -> Self:
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            orgName = model.orgName,
            location = model.location,
            date = model.date,
            time = model.time
        )
    
    def to_model(self) -> Event:
        return Event(
            id = self.id,
            name = self.name,
            orgName = self.orgName,
            location = self.location,
            description = self.description,
            date = self.date,
            time = self.time
        )

