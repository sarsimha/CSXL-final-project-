import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Route } from '@angular/router';
import { Observable } from 'rxjs';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { EventRegService, Event } from './event-reg.service';

@Component({
  selector: 'app-event-reg',
  templateUrl: './event-reg.component.html',
  styleUrls: ['./event-reg.component.css']
})
export class EventRegComponent {
  public static Route: Route = {
    path: 'event_reg',
    component: EventRegComponent,
    title: 'Event Registration', 
    canActivate: [isAuthenticated], 
  }
  // public events$: Observable<Event[]>

  constructor(
    private eventRegService: EventRegService,
    private formBuilder: FormBuilder,
    route: ActivatedRoute, 
  ) {
  }

  eventForm = this.formBuilder.group({
    name: '',
    orgName: '',
    location: '',
    description: '',
    date: '',
    time: ''
  });


  onSubmit(): void {
    // console.log('start submit')
    let form = this.eventForm.value;
    let name = form.name ?? "";
    let orgName = form.orgName ?? "";
    let location = form.location ?? "";
    let description = form.description ?? "";
    let date = form.date ?? "";
    let time = form.time ?? "";

    this.eventRegService
      .createEvent(name, orgName, location, description, date, time)
      .subscribe({
        next: (event) => this.onSuccess(event),
        error: (err) => this.onError(err)
      });
  }

  private onSuccess(event: Event): void {
    // console.log("scces")
    window.alert(`Thanks for registering your event: ${event.name}`);
    this.eventForm.reset();
  }

  private onError(err: Error) {
    if (err.message) {
      window.alert(err.message);
    } else {
      window.alert("Unknown error: " + JSON.stringify(err));
    }
  }
}
