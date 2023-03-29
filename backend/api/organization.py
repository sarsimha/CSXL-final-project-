from fastapi import APIRouter, Depends
from ..services import OrganizationService
from ..models import Organization

api = APIRouter(prefix="/api/organization")


@api.get("", response_model=list[Organization], tags=['Organization'])
def get_orgs(org_svc: OrganizationService = Depends()) -> list[Organization]:
    return org_svc.all()
