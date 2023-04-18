import { Component, ViewChild, OnInit } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { Observable, of } from 'rxjs';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { Event, EventService } from './event.service';
import { Organization, OrganizationsService } from '../organizations/organizations.service';
import { FormControl } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';


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

  constructor(route: ActivatedRoute, private eventService: EventService, private orgService: OrganizationsService) {
    this.allEvents$ = eventService.getAllEvents()
    this.organizations$ = orgService.getAllOrganizations()
    
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
}
