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

We have created the following data models
- Organization: a model for Student Organization that has the id, name, and description. 
- Event: 

*TODO: Add all data models created in the final project, update as needed*

## Viewing Student Organizations

### Backend Logic

For development purposes, we created dummy organization objects that is initalized once running `backend/script/reset_database`. 

#### API
`backend/api/organization.py` creates the api routes and method `get_orgs()` to retrieve all existing organizations.

#### Services
`backend/services/organization.py` creates the Organization Service that has a method called `all()` that calls SQL query to parse all Organization Entities in the list that returns the equivalent Organization Models. 

### Frontend

*TODO: Documentation on frontend implementation for viewing orgs*

## Viewing Events

*TODO: Documentation on backend and frontend implementation for viewing events*

## Creating Events

*TODO: Documentation on backend and frontend implementation for creating events*
