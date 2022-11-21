import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TargetsLocationGraphComponent } from './targets-location-graph.component';

describe('TargetsLocationGraphComponent', () => {
  let component: TargetsLocationGraphComponent;
  let fixture: ComponentFixture<TargetsLocationGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TargetsLocationGraphComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TargetsLocationGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
