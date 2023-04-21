# Student Organizations Feature

Authors: Cecilia Lee, Kelly Fan, Sarika Simha, Sonika Puvvada

## Table of Contents

* [Purpose of Feature](#purpose-of-feature)
* [Data Models](#data-models)
* [Viewing Student Organizations](#viewing-student-organizations)
* [Viewing Events](#viewing-events)
* [Creating Events](#creating-events)

## Purpose of Feature

The student organizations achieve the following user stories:

- As Sol Student, view a list of student organizations and their details
- As Sol Student, view a list of events hosted by student organizations
- As Eli Exec, fill out a form to create an event hosted by their student organization

## Data Models

We have created the following data models:
- Organization: a model for Student Organization that has the id, name, and description. 
- Event: a model for an Event created by a Student Organization that has the event name, description, organization, location, date, and time.

## Viewing Student Organizations

### Backend Logic
For development purposes, we created three dummy organization objects, `pearl_hacks`, `app_team`, and `black_technology`, that are initalized once running `backend/script/reset_database`.

#### API
`backend/api/organization.py` creates the API routes and method `get_orgs()` to retrieve all existing organizations.

#### Services
`backend/services/organization.py` creates the Organization Service that has method `all()` that calls SQL query to parse all Organization Entities in the list that returns the equivalent Organization Models. 

### Frontend
The folder `frontend/src/app/organizations` contains the implementation for viewing organizations.
`organizations.service.ts` creates the Organizations Service that has a method `getAllOrganizations()` that makes an HTTP GET request to return the list of organizations.

## Viewing Events

### Backend Logic
For development purposes, we created dummy event objects that are initalized once running `backend/script/reset_database`.

#### API
`backend/api/event.py` creates the API routes and method `get_events()` to retrieve all existing events.

#### Services
`backend/services/event.py` creates the Event Service that has method `all()` that calls SQL query to parse all Event Entities in the list that returns the equivalent Event Models. 

### Frontend
The folder `frontend/src/app/event` contains the implementation for viewing events.
`event.service.ts` creates the Events Service that has a method `getAllEvents()` that makes an HTTP GET request to return the list of events.

## Creating Events

### Backend logic

In order to ensure that only Organization Executives are able to create a new event into the database, we created a new 'Eli Executive' user in `backend/script/dev_data/users.py` with a role defined in `backend/script/dev_data/roles.py` as an 'Organization Executive', binded as a pair in `backend/script/dev_data/user_roles.py`. We add a permission to create an event in `backend/script/dev_data/permissions.py` for the organization executive role. 

#### API
`backend/api/event.py` creates the API routes and method `create_event()` to create a new event and add to the existing event database while checking if the user is an Eli Exec. 

#### Services
`backend/services/event.py` creates the Event Service and has method `create_event()` that calls SQL query to create a new Event Entity then adds it to the session and returns the equivalent Event Model. This only happens if the user is an Eli Exec. 

### Frontend
The folder `frontend/src/app/event-reg` contains the implementation for creating events.
`event-reg.service.ts` creates the EventReg Service that has a method `createEvent(name: string, orgName: string, location: string, description: string, date: string, time: string)` that makes an HTTP POST request to create a new event. 

Frontend dependencies:
1. `npm install angular-mat-datepicker`
2. `npm install --save ngx-material-timepicker`
