import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AgendaComponent } from './agenda';

describe('AgendaComponent', () => {
  let component: AgendaComponent;
  let fixture: ComponentFixture<AgendaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AgendaComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AgendaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('should display agenda items', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelectorAll('.agenda-item').length).toBe(component.agenda.length);
    expect(compiled.querySelector('.agenda-time')).toBeTruthy();
    expect(compiled.querySelector('.agenda-title')).toBeTruthy();
  });
});