import pytest

from sqlalchemy.orm import Session
from ...models import Event
from ...entities import EventEntity
from ...services import EventService

# Mock Models, same from dev data

tie_dye_social = Event(id=301, name='Tie Dye Social', orgName='Pearl Hacks', location='fb011',
                        description='Come meet other hackers and tie-dye a Pearl Hacks shirt in your favorite color.', 
                        date='04/12/2023', time='06:00PM')

networking_csxl = Event(id=302, name='Networking with CSXL', orgName='App Team', location='fb023',
                        description='Come meet the CSXL team.', 
                        date='04/13/2023', time='06:30PM')

bofa_panel = Event(id=303, name='Bank of America Panel', orgName='Black in Technology', location='fb008',
                        description='Hear from current developers at Bank of America and ask questions.', 
                        date='04/14/2023', time='05:30PM')


models = [
    tie_dye_social,
    networking_csxl,
    bofa_panel
]

@pytest.fixture(autouse=True)
def setup_teardown(test_session: Session):
    # Add test events to session
    testEvent1 = EventEntity.from_model(tie_dye_social)
    testEvent2 = EventEntity.from_model(networking_csxl)
    testEvent3 = EventEntity.from_model(bofa_panel)
    test_session.add(testEvent1)
    test_session.add(testEvent2)
    test_session.add(testEvent3)
    test_session.commit()
    

@pytest.fixture()
def event(test_session: Session):
    return EventService(test_session)


def test_get_all_event(event: EventService):
    """ Retrieves all dummy data using Event Service """
    assert len(event.all()) == 3
    
def test_create_event_added(event: EventService):
    """ Create one event, check added to event database """

    new_event = Event(
        name="Resume and Snacks",
        orgName="Pearl Hacks",
        location="fb001",
        description="Bring your resume to discuss with recruiters over snacks",
        date="04/16/2023",
        time="06:30PM"
    )

    event.create_event(new_event)
    assert len(event.all()) == 4

def test_create_event_position(event: EventService):
    """ Create one event, check position added to database """

    new_event = Event(
        name="Resume and Snacks",
        orgName="Pearl Hacks",
        location="fb001",
        description="Bring your resume to discuss with recruiters over snacks",
        date="04/13/2023",
        time="05:30PM"
    )

    event.create_event(new_event)
    assert event.all()[3].name == "Resume and Snacks"