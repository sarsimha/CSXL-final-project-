import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { Observable } from 'rxjs';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { Event, EventService } from './event.service';


@Component({
  selector: 'app-event',
  templateUrl: './event.component.html',
  styleUrls: ['./event.component.css']
})
export class EventComponent {
  public static Route: Route = {
    path: 'event',
    component: EventComponent,
    title: 'Events',
    canActivate: [isAuthenticated],
  }
  public allEvents$: Observable<Event[]>

  constructor(route: ActivatedRoute, private eventService: EventService) {
    this.allEvents$ = eventService.getAllEvents()
  }
}