import { ComponentFixture, TestBed } from '@angular/core/testing';
import { UpdatesComponent } from './updates';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('UpdatesComponent', () => {
  let component: UpdatesComponent;
  let fixture: ComponentFixture<UpdatesComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UpdatesComponent],
      imports: [HttpClientTestingModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdatesComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  afterEach(() => {
    // Garante que todas as requests são tratadas ANTES do verify
    httpMock.verify();
  });

  it('deve criar o componente', () => {
    // Mock da request feita no ngOnInit (evita erro de request pendente!)
    httpMock.expectOne('/live/updates').flush([]);
    expect(component).toBeTruthy();
  });

  it('deve carregar atualizações no init', () => {
    const mockUpdates = [
      { id: 1, message: 'Primeira atualização', timestamp: '2025-08-26T18:01:00Z', type: 'INFO' },
      { id: 2, message: 'Segunda atualização', timestamp: '2025-08-26T18:02:00Z' }
    ];

    const req = httpMock.expectOne('/live/updates');
    expect(req.request.method).toBe('GET');
    req.flush(mockUpdates);

    expect(component.updates.length).toBe(2);
    expect(component.loading).toBeFalse();
    expect(component.errorMsg).toBe('');
  });

  it('deve mostrar erro se falhar o carregamento das atualizações', () => {
    const req = httpMock.expectOne('/live/updates');
    req.error(new ErrorEvent('Network error'));

    expect(component.errorMsg).toBe('Erro ao carregar atualizações.');
    expect(component.loading).toBeFalse();
    expect(component.updates.length).toBe(0);
  });
});