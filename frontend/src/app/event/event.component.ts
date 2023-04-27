import { Component, ViewChild, OnInit } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { Observable, of, map, switchMap } from 'rxjs';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { Event, EventService } from './event.service';
import { Organization, OrganizationsService } from '../organizations/organizations.service';
import { PermissionService } from '../permission.service';
import { ConfirmDeleteService } from './confirm-delete/confirm-delete.service';
import { FormControl } from '@angular/forms';


@Component({
  selector: 'app-event',
  templateUrl: './event.component.html',
  styleUrls: ['./event.component.css']
})
export class EventComponent {
  public displayedColumns = ['event', 'description', 'location', 'org-name', 'date', 'time'];

  public static Route: Route = {
    path: 'event',
    component: EventComponent,
    title: 'Events',
    canActivate: [isAuthenticated],
  }
  
  public allEvents$: Observable<Event[]>
  public orderedEvents$: Observable<Event[]>

  // For the filter by organization drop down
  public organizations$: Observable<Organization[]>;
  public org: any;
  public orgControl = new FormControl('');
  public execPermission$: Observable<boolean>;

  constructor(
    route: ActivatedRoute, 
    private eventService: EventService, 
    private orgService: OrganizationsService,
    private permission: PermissionService,
    private confirmDelete: ConfirmDeleteService
    ) {
    this.allEvents$ = eventService.getAllEvents()
    this.orderedEvents$ = eventService.getAllEvents()
    this.orderEvents()
    this.organizations$ = orgService.getAllOrganizations()
    this.execPermission$ = this.permission.check('event.delete_event', 'event/delete/')

    this.execPermission$.subscribe(permission => {
      if (permission) {
        this.displayedColumns.push('delete')
      }
    });
  }

  public searchOrganizations(org: string) {
    this.eventService.searchEventByOrganization(org)
      .subscribe(data => {
        this.allEvents$ = of(data);
      });
  }

  public getAllEvents() {
    this.eventService.getAllEvents()
      .subscribe(data => {
        this.allEvents$ = of(data);
      });
  }

  public deleteEvent(eventId: number, eventName: string) {
    //add pop-up check to confirm event deletion
    this.confirmDelete.confirm(
      `Delete ${eventName}.`, 
      `This action is final.`)
      .pipe(switchMap(outcome => {
        if (outcome === true) {
          //reload so user doesn't face "500 internal service error" pop-up
          window.location.reload()
          //delete event
          return this.eventService.deleteEvent(eventId);
        }
        else {
          return this.eventService.getAllEvents();
        }
      })).subscribe(() => {
          this.allEvents$ = this.eventService.getAllEvents();
        });
  }

  public orderEvents() {
    this.orderedEvents$
      .subscribe((list) =>
        list.sort((a, b) =>
          new Date(a.date).setHours(0,0,0,0) < new Date(b.date).setHours(0,0,0,0) ? -1 :
          new Date(a.date).setHours(0,0,0,0) > new Date(b.date).setHours(0,0,0,0) ? 1 :
          0
      ));
    
      this.orderedEvents$
      .subscribe((list) =>
        list.forEach((event) => {
          console.log(event.date)
        }));
  }
}
