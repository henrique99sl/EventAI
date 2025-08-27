import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AgendaComponent } from './agenda.component';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('AgendaComponent', () => {
  let component: AgendaComponent;
  let fixture: ComponentFixture<AgendaComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AgendaComponent],
      imports: [HttpClientTestingModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AgendaComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('deve criar o componente', () => {
    // Mock da request feita no ngOnInit (evita erro de request pendente!)
    httpMock.expectOne('/events/calendar').flush([]);
    expect(component).toBeTruthy();
  });

  it('deve carregar eventos no ngOnInit', () => {
    const mockEvents = [
      { id: 1, title: 'Evento 1', date: '2025-09-01', location: 'Lisboa' },
      { id: 2, title: 'Evento 2', date: '2025-09-02', time: '14:00', location: 'Porto', description: 'Descrição do evento' }
    ];

    // Espera pela chamada HTTP e responde com mock
    const req = httpMock.expectOne('/events/calendar');
    expect(req.request.method).toBe('GET');
    req.flush(mockEvents);

    expect(component.events.length).toBe(2);
    expect(component.loading).toBeFalse();
    expect(component.errorMsg).toBe('');

    // Verifica se os eventos aparecem no template
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Evento 1');
    expect(compiled.textContent).toContain('Evento 2');
  });

  it('deve mostrar mensagem de erro se falhar o carregamento', () => {
    const req = httpMock.expectOne('/events/calendar');
    req.error(new ErrorEvent('Network error'));

    expect(component.errorMsg).toBe('Erro ao carregar agenda.');
    expect(component.loading).toBeFalse();
    expect(component.events.length).toBe(0);

    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Erro ao carregar agenda.');
  });
});