import { ComponentFixture, TestBed } from '@angular/core/testing';
import { VotingComponent } from './voting';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';
import { By } from '@angular/platform-browser';

describe('VotingComponent', () => {
  let component: VotingComponent;
  let fixture: ComponentFixture<VotingComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [VotingComponent],
      imports: [HttpClientTestingModule, FormsModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VotingComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('deve criar o componente', () => {
    // Mock da request feita no ngOnInit para evitar request pendente!
    httpMock.expectOne('/live/voting/options').flush([]);
    expect(component).toBeTruthy();
  });

  it('deve carregar opções no init', () => {
    const mockOptions = [
      { id: 1, label: 'Opção 1', votes: 10 },
      { id: 2, label: 'Opção 2', votes: 5 }
    ];

    const req = httpMock.expectOne('/live/voting/options');
    expect(req.request.method).toBe('GET');
    req.flush(mockOptions);

    expect(component.options.length).toBe(2);
    expect(component.options[0].label).toBe('Opção 1');
  });

  it('deve enviar voto e mostrar sucesso', () => {
    // Mock da request de opções inicial do ngOnInit
    httpMock.expectOne('/live/voting/options').flush([{ id: 1, label: 'Opção 1', votes: 10 }]);

    component.selectedOptionId = 1;
    fixture.detectChanges();

    component.vote();

    const reqVote = httpMock.expectOne('/live/voting/vote');
    expect(reqVote.request.method).toBe('POST');
    reqVote.flush({});

    // Depois de votar, atualiza opções
    const reqOptions = httpMock.expectOne('/live/voting/options');
    reqOptions.flush([{ id: 1, label: 'Opção 1', votes: 11 }]);

    expect(component.successMsg).toBe('Voto registado!');
    expect(component.submitting).toBeFalse();
    expect(component.options[0].votes).toBe(11);
  });

  it('deve mostrar erro ao falhar o envio do voto', () => {
    // Mock da request de opções inicial do ngOnInit
    httpMock.expectOne('/live/voting/options').flush([{ id: 1, label: 'Opção 1', votes: 10 }]);

    component.selectedOptionId = 1;
    fixture.detectChanges();

    component.vote();

    const reqVote = httpMock.expectOne('/live/voting/vote');
    reqVote.error(new ErrorEvent('Network error'));

    expect(component.errorMsg).toBe('Erro ao enviar voto.');
    expect(component.submitting).toBeFalse();
  });

  it('deve desabilitar botão se enviando ou nada selecionado', () => {
    // Mock da request de opções inicial do ngOnInit
    httpMock.expectOne('/live/voting/options').flush([{ id: 1, label: 'Opção 1', votes: 10 }]);

    component.selectedOptionId = null;
    fixture.detectChanges();
    const button = fixture.debugElement.query(By.css('button')).nativeElement;
    expect(button.disabled).toBeTrue();

    component.selectedOptionId = 1;
    component.submitting = true;
    fixture.detectChanges();
    expect(button.disabled).toBeTrue();
  });
});