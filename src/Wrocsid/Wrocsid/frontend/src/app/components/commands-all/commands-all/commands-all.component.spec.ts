import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommandsAllComponent } from './commands-all.component';

describe('CommandsAllComponent', () => {
  let component: CommandsAllComponent;
  let fixture: ComponentFixture<CommandsAllComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CommandsAllComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CommandsAllComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
