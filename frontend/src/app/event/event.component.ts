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
  public orderedEventsList: Event[] = []

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
    this.allEvents$ = this.orderEvents()    
    this.organizations$ = orgService.getAllOrganizations()
    this.execPermission$ = this.permission.check('event.delete_event', 'event/delete/')

    this.execPermission$.subscribe(permission => {
      if (permission) {
        this.displayedColumns.push('delete')
      }
    });
  }

  public searchOrganizations(org: string) {
    // get events of an org that are ordered by date
    this.eventService.searchEventByOrganization(org)
      .subscribe(data => {
        this.allEvents$ = of(
          data.sort((a, b) =>
          new Date(a.date).setHours(Number(a.time.slice(0,2)), Number(a.time.slice(3,5)), 0, 0) 
          - new Date(b.date).setHours(Number(b.time.slice(0,2)), Number(b.time.slice(3,5)), 0, 0)
        ));
      });
  }

  public getAllEvents() {
    // get all events ordered by date
    this.eventService.getAllEvents()
      .subscribe(data => {
        this.allEvents$ = of(
          data.sort((a, b) =>
          new Date(a.date).setHours(Number(a.time.slice(0,2)), Number(a.time.slice(3,5)), 0, 0) 
          - new Date(b.date).setHours(Number(b.time.slice(0,2)), Number(b.time.slice(3,5)), 0, 0)
        ));
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
          this.allEvents$ = this.orderEvents();
        });
  }

  public orderEvents() {
    // order all events by date
    return this.allEvents$.pipe(
      map((list) => {
        list.sort((a, b) =>
        new Date(a.date).setHours(Number(a.time.slice(0,2)), Number(a.time.slice(3,5)), 0, 0) 
        - new Date(b.date).setHours(Number(b.time.slice(0,2)), Number(b.time.slice(3,5)), 0, 0)
        );
        return list;
      })
    );
  }
  
}
