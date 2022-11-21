import { TestBed } from '@angular/core/testing';

import { WrocsidService } from './wrocsid.service';

describe('WrocsidService', () => {
  let service: WrocsidService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WrocsidService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
