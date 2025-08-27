import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EventListComponent, EventItem } from './event-list';

describe('EventListComponent', () => {
  let component: EventListComponent;
  let fixture: ComponentFixture<EventListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EventListComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EventListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display events', () => {
    const events: EventItem[] = [
      { id: 1, title: 'Evento 1', date: '2025-09-01', location: 'Lisboa' },
      { id: 2, title: 'Evento 2', date: '2025-09-02', time: '14:00', location: 'Porto', description: 'Descrição do evento' }
    ];
    component.events = events;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelectorAll('li').length).toBe(2);
    expect(compiled.textContent).toContain('Evento 1');
    expect(compiled.textContent).toContain('Lisboa');
    expect(compiled.textContent).toContain('Evento 2');
    expect(compiled.textContent).toContain('Descrição do evento');
  });

  it('should show empty message when no events', () => {
    component.events = [];
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.empty')?.textContent).toContain('Sem eventos para mostrar.');
  });
});