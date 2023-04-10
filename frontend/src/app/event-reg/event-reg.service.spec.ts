import { TestBed } from '@angular/core/testing';

import { EventRegService } from './event-reg.service';

describe('EventRegService', () => {
  let service: EventRegService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EventRegService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
