import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AssistantWidgetComponent } from './assistant-widget';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';

describe('AssistantWidgetComponent', () => {
  let component: AssistantWidgetComponent;
  let fixture: ComponentFixture<AssistantWidgetComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AssistantWidgetComponent],
      imports: [HttpClientTestingModule, FormsModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AssistantWidgetComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should send message and receive response', () => {
    component.userMessage = 'Olá assistente!';
    component.sendMessage();

    const req = httpMock.expectOne('/assistant');
    expect(req.request.method).toBe('POST');
    req.flush({ reply: 'Olá! Como posso ajudar?' });

    expect(component.conversation.length).toBe(2);
    expect(component.conversation[1].from).toBe('assistant');
    expect(component.conversation[1].message).toBe('Olá! Como posso ajudar?');
  });

  it('should show error on backend failure', () => {
    component.userMessage = 'Pergunta com erro';
    component.sendMessage();

    const req = httpMock.expectOne('/assistant');
    req.error(new ErrorEvent('Network error'));

    expect(component.conversation[1].from).toBe('assistant');
    expect(component.conversation[1].message).toContain('Erro ao contactar o assistente.');
  });
});