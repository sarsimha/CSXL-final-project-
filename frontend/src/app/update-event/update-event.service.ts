import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { mergeMap, Observable, of, shareReplay, throwError} from 'rxjs';
import { catchError, map, find, filter } from 'rxjs/operators';

export interface Event {
  // id?: number
  name: string;
  orgName: string;
  location: string;
  description: string;
  date: string;
  time: string;
}

@Injectable({
  providedIn: 'root'
})
export class UpdateEventService {
  public events$: Observable<Event[] | undefined>;

  constructor(private http: HttpClient, protected auth: AuthenticationService) { 
    this.events$ = this.auth.isAuthenticated$.pipe(
      mergeMap(isAuthenticated => {
        if (isAuthenticated) {
          return this.getEvents()
        } else {
          return of(undefined);
        }
      }),
      shareReplay(1)
    );
  }

  getEvents(): Observable<Event[]> {
    return this.http.get<Event[]>("/api/event");
  }

  // searchEventByName(event: string): Observable<Event[]> {
  //   return this.http.get<Event[]>(`/api/event/${event}`).pipe(
  //     map(data => {
  //       return data;
  //     }),
  //     catchError((error: any) => {
  //       console.error(error);
  //       return of();
  //     }),
  //   );
  // }

  // getEventId(event: string): number {
  //   let events_list$ = this.getEvents()
  //   // return events_list$.pipe(map(events_list$ => events_list$.filter(x => x.event === event)));
  //   // return events_list$.filter(x=> x.event === event);
  // }

  updateEvent(eventId: number, name: string, orgName: string, location: string, description: string, date: string, time: string): Observable<Event> {
    let errors: string[] = [];

    if (name === "") {
      errors.push(`Event Name required.`);
    }

    if (orgName === "") {
      errors.push(`Organization Name required.`)
    }

    if (location === "") {
      errors.push(`Location required.`)
    }

    if (description === "") {
      errors.push(`Description required.`)
    }

    
    if (date.toString() === 'Invalid Date') {
      errors.push(`Date required.`)
    }

    if (time === "") {
      errors.push(`Time required.`)
    }

    if (errors.length > 0) {
      return throwError(() => { return new Error(errors.join("\n")) });
    }

    // display only the date portion
    date = date.toString().substring(4,15)
    
    let event: Event = {name, orgName, location, description, date, time};

    // this.http.delete<Event>("/api/event/delete")
    // return this.http.put<Event>("/api/event/update", event)
    return this.http.put<Event>(`/api/event/update/${eventId}`, event);
    // return this.http.post<Event>("/api/event/create", event)
  }
}
