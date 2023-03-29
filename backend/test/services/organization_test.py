import pytest

from sqlalchemy.orm import Session
from ...models import Organization
from ...entities import OrganizationEntity
from ...services import OrganizationService

# Mock Models, same from dev data

pearl_hacks = Organization(id=101, name="Pearl Hacks", 
                           description="Hackathon for women and gender non-conforming students."
                           )

app_team = Organization(id=102, name="App Team Carolina", 
                        description="A club that provides a collaborative environment for UNC students to learn iOS development."
                        )

black_technology = Organization(id=103, name="Black in Technology", 
                                description="A supportive network for the academic and professional development of Black students in tech majors at UNC."
                                )

@pytest.fixture(autouse=True)
def setup_teardown(test_session: Session):
    # Add test organizations to session
    test_org = OrganizationEntity.from_model(pearl_hacks)
    test_org_1 = OrganizationEntity.from_model(app_team)
    test_org_2 = OrganizationEntity.from_model(black_technology)
    test_session.add(test_org)
    test_session.add(test_org_1)
    test_session.add(test_org_2)
    test_session.commit()
    

@pytest.fixture()
def permission(test_session: Session):
    return OrganizationService(test_session)


def test_get_all_org(permission: OrganizationService):
    """ Retrieves all dummy data using Organization Service """
    assert len(permission.all()) == 3
    