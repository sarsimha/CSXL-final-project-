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
      `This action is final.`).pipe(
        switchMap(res => {
          if (res === true) {
            return this.eventService.deleteEvent(eventId);
          }
          else {
            //idk what else to put
            return this.eventService.getAllEvents();
          }
        })).subscribe(() => {
            //reload so user doesn't face "500 internal service error" pop-up
            window.location.reload()
            this.allEvents$ = this.eventService.getAllEvents();
          });
    
    // simple implementation
    // if(confirm(`Are you sure you want to delete ${eventName}?`)) {
    //   this.eventService.deleteEvent(eventId)
    //     .subscribe(() => {
    //       this.allEvents$ = this.eventService.getAllEvents();
    //     });
    //   //reload so user doesn't face "500 internal service error" pop-up
    //   window.location.reload()
    // }
  }
}
