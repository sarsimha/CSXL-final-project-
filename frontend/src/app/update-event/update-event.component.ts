import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { permissionGuard } from '../permission.guard';
import { Organization, OrganizationsService } from '../organizations/organizations.service';
import { UpdateEventService, Event } from './update-event.service';
import { EventService } from '../event/event.service';
import { identifierName } from '@angular/compiler';

@Component({
  selector: 'app-update-event',
  templateUrl: './update-event.component.html',
  styleUrls: ['./update-event.component.css']
})
export class UpdateEventComponent {
  public static Route: Route = {
    path: 'update_event',
    component: UpdateEventComponent,
    title: 'Update Event Form', 
    // only eli exec (and root) able to access page, otherwise redirect
    canActivate: [permissionGuard('event.update_event', 'event/update/')]
  }
  public organizations$: Observable<Organization[]>;
  public events$: Observable<Event[]>;
  public events_dict: {[name: string] : number | undefined} = {}


    //create dict with name and id
    public getEventsDict(): void {
      this.events$
      .subscribe(data => {
        data.forEach((x) => {
        this.events_dict[x.name] = x.id
      })
      });
    }

  constructor(
    private updateEventService: UpdateEventService,
    private formBuilder: FormBuilder,
    private orgService: OrganizationsService,
    private eventService: EventService,
    route: ActivatedRoute
  ) {
    this.organizations$ = orgService.getAllOrganizations();
    this.events$ = eventService.getAllEvents();
    this.getEventsDict()
  }

  updateEventForm = this.formBuilder.group({
    name: '',
    orgName: '',
    location: '',
    description: '',
    date: '',
    time: ''
  });

  onSubmit(): void {
    let form = this.updateEventForm.value;
    let name = form.name ?? "";
    let orgName = form.orgName ?? "";
    let location = form.location ?? "";
    let description = form.description ?? "";
    let date = form.date ?? "";
    let time = form.time ?? "";
    let eventId = this.events_dict[name]!

    this.updateEventService
      .updateEvent(eventId, name, orgName, location, description, date, time)
      .subscribe({
        next: (event) => this.onSuccess(event),
        error: (err) => this.onError(err)
      });
  }

  private onSuccess(event: Event): void {
    window.alert(`Thanks for updating your event: ${event.name}`);
    this.updateEventForm.reset();
    // refresh event page so that it shows updated event, 
    // but it might already do that when you go to the events page
  }

  private onError(err: Error) {
    if (err.message) {
      window.alert(err.message);
    } else {
      window.alert("Unknown error: " + JSON.stringify(err));
    }
  }
}
