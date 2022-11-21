import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommandsResultsComponent } from './commands-results.component';

describe('CommandsResultsComponent', () => {
  let component: CommandsResultsComponent;
  let fixture: ComponentFixture<CommandsResultsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CommandsResultsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CommandsResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
