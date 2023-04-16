from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Organization
from ..entities import OrganizationEntity


class OrganizationService:

    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def all(self) -> list[Organization] | None:
        """List Organizations from database.

        Returns:
            list[Organization] | None: The list of organizations or None if not found."""
        query = select(OrganizationEntity)
        org_entities: list[OrganizationEntity] = self._session.scalars(query).all()
        if org_entities is None:
            return None
        else:
            return [entity.to_model() for entity in org_entities]