import { ComponentFixture, TestBed } from '@angular/core/testing';
import { StatsComponent } from './stats';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('StatsComponent', () => {
  let component: StatsComponent;
  let fixture: ComponentFixture<StatsComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [StatsComponent],
      imports: [HttpClientTestingModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StatsComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('deve criar o componente', () => {
    // Mock da request feita no ngOnInit (evita erro de request pendente!)
    httpMock.expectOne('/live/stats').flush(null);
    expect(component).toBeTruthy();
  });

  it('deve buscar e exibir estatísticas', () => {
    const mockStats = {
      viewers: 123,
      messages: 45,
      votes: 6,
      updatedAt: '2025-08-26T18:00:00Z'
    };

    const req = httpMock.expectOne('/live/stats');
    expect(req.request.method).toBe('GET');
    req.flush(mockStats);

    expect(component.stats).toEqual(mockStats);
    expect(component.loading).toBeFalse();
    expect(component.errorMsg).toBe('');
  });

  it('deve mostrar erro se falhar ao buscar estatísticas', () => {
    const req = httpMock.expectOne('/live/stats');
    req.error(new ErrorEvent('Network error'));

    expect(component.errorMsg).toBe('Erro ao carregar estatísticas.');
    expect(component.loading).toBeFalse();
    expect(component.stats).toBeNull();
  });
});