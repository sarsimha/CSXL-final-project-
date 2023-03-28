'''Organizations for all registered organizations in the application'''


from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from ..models import Organization


class OrganizationEntity(EntityBase):
    __tablename__ = 'organization'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[int] = mapped_column(String(32), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(128), unique=True, index=True)

    @classmethod
    def from_model(cls, model: Organization) -> Self:
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
        )

    def to_model(self) -> Organization:
        return Organization(
            id=self.id,
            name=self.name,
            description=self.description,
        )

    def update(self, model: Organization) -> None:
        self.name = model.name
        self.description = model.description
