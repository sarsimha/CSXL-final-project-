import pytest

from sqlalchemy.orm import Session
from ...models import User, Role, Permission, Event, EventForm
from ...entities import UserEntity, RoleEntity, PermissionEntity, EventEntity
from ...services import PermissionService, EventService, UserPermissionError


# Mock Models for Users 
executive = User(id=3, pid=777777777, onyen='executive', email='executive@unc.edu')
executive_role = Role(id=3, name='executive')
executive_permission: Permission

ambassador = User(id=2, pid=888888888, onyen='ambassador',
                  email='ambassador@unc.edu')
ambassador_role = Role(id=2, name='ambassadors')
ambassador_permission: Permission

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

    # Bootstrap executive and role
    executive_entity = UserEntity.from_model(executive)
    test_session.add(executive_entity)
    executive_role_entity = RoleEntity.from_model(executive_role)
    executive_role_entity.users.append(executive_entity)
    test_session.add(executive_role_entity)
    executive_permission_entity = PermissionEntity(
        action='event.*', resource='*', role=executive_role_entity)
    test_session.add(executive_permission_entity)

    # Bootstrap ambassador and role
    ambassador_entity = UserEntity.from_model(ambassador)
    test_session.add(ambassador_entity)
    ambassador_role_entity = RoleEntity.from_model(ambassador_role)
    ambassador_role_entity.users.append(ambassador_entity)
    test_session.add(ambassador_role_entity)
    ambassador_permission_entity = PermissionEntity(
        action='checkin.create', resource='checkin', role=ambassador_role_entity)
    test_session.add(ambassador_permission_entity)

    test_session.commit()

    global executive_permission
    executive_permission = executive_permission_entity.to_model()
    global ambassador_permission
    ambassador_permission = ambassador_permission_entity.to_model()
    yield
    

@pytest.fixture()
def permission(test_session: Session):
    return PermissionService(test_session)


@pytest.fixture()
def event(test_session: Session, permission: PermissionService):
    # add permission to event
    return EventService(test_session, permission)


def test_get_all_event(event: EventService):
    """ Retrieves all dummy data using Event Service """
    assert len(event.all()) == 3
    
def test_create_event_added(event: EventService):
    """ Without checking current user's permissions, create one event and check if added to event database """

    new_event = Event(
        name="Resume and Snacks",
        orgName="Pearl Hacks",
        location="fb001",
        description="Bring your resume to discuss with recruiters over snacks",
        date="04/16/2023",
        time="06:30PM"
    )

    event.create_event(None, new_event)
    assert len(event.all()) == 4

def test_create_event_position(event: EventService):
    """ Without checking current user's permissions, create one event and check position added to event database """

    new_event = Event(
        name="Resume and Snacks",
        orgName="Pearl Hacks",
        location="fb001",
        description="Bring your resume to discuss with recruiters over snacks",
        date="04/13/2023",
        time="05:30PM"
    )

    event.create_event(None, new_event)
    assert event.all()[3].name == "Resume and Snacks"

def test_executive_can_create_event(event: EventService):
    """ Check executive able to create one event """

    newEvent = Event(
        name="Test event",
        orgName="Test org",
        location="Test location",
        description="Test decription",
        date="11/11/1111",
        time="11:59PM"
    )

    event.create_event(executive, newEvent)
    assert len(event.all()) == 4

def test_ambassador_cannot_create_event(event: EventService):
    """ Check ambassador, without create_event permission, not able to create one event """

    newEvent = Event(
        name="Test event",
        orgName="Test org",
        location="Test location",
        description="Test decription",
        date="11/11/1111",
        time="11:59PM"
    )
    
    try:
        event.create_event(ambassador, newEvent)
        assert False
    except UserPermissionError:
        assert True

def test_delete_event(event: EventService):
    """ Check executive able to delete one event """

    event.delete_event(executive, networking_csxl.id)
    assert len(event.all()) == 2

def test_ambassador_cannot_delete_event(event: EventService):
    """ Check ambassador not able to delete one event """

    try:
        event.delete_event(ambassador, networking_csxl.id)
        assert False
    except UserPermissionError:
        assert True

def test_get_event(event: EventService):
    """ Check executive able to get event by id """

    event.get_event(executive, 301)
    assert event.all()[0].id == 301

def test_ambassador_cannot_get_event(event: EventService):
    """ Check ambassador not able to get event """

    try:
        event.get_event(ambassador, 301)
        assert False
    except UserPermissionError:
        assert True

def test_update_event(event: EventService):
    """ Check executive able to update an event"""
    editEvent = Event(id=301, name='Tie Dye Social', orgName='Pearl Hacks', location='fb011',
                        description='Come meet other hackers and tie-dye a Pearl Hacks shirt in your favorite color.', 
                        date='04/12/2023', time='19:00')
    event.update_event(executive, editEvent)
    assert event.get_event(executive, 301) == editEvent

def test_ambassador_cannot_update_event(event: EventService):
    """ Check ambassador not able to edit/udpdate event """
    editEvent = Event(id=301, name='Tie Dye Social', orgName='Pearl Hacks', location='fb011',
                        description='Come meet other hackers and tie-dye a Pearl Hacks shirt in your favorite color.', 
                        date='04/12/2023', time='19:00')
    try:
        event.update_event(ambassador, editEvent)
        assert False
    except UserPermissionError:
        assert True
