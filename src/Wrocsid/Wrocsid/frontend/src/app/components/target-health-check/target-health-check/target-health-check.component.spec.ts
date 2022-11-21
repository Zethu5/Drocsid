import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TargetHealthCheckComponent } from './target-health-check.component';

describe('TargetHealthCheckComponent', () => {
  let component: TargetHealthCheckComponent;
  let fixture: ComponentFixture<TargetHealthCheckComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TargetHealthCheckComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TargetHealthCheckComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
