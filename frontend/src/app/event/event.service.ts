import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { mergeMap, Observable, of, shareReplay } from 'rxjs';


export interface Event {
  id?: number
  name: string
  orgName: string
  location: string
  description: string
  date: string
  time: string
}
@Injectable({
  providedIn: 'root'
})
export class EventService {
  public event$: Observable<Event[] | undefined>;

  constructor(protected http: HttpClient, protected auth: AuthenticationService) {
    this.event$ = this.auth.isAuthenticated$.pipe(
      mergeMap(isAuthenticated => {
        if (isAuthenticated) {
          return this.getAllEvents()
        } else {
          return of(undefined);
        }
      }),
      shareReplay(1)
    );
  }

  // Returns all events from database
  getAllEvents(): Observable<Event[]> {
    return this.http.get<Event[]>('/api/event')
  }

}
