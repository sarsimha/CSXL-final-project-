import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventRegComponent } from './event-reg.component';

describe('EventRegComponent', () => {
  let component: EventRegComponent;
  let fixture: ComponentFixture<EventRegComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EventRegComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EventRegComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
