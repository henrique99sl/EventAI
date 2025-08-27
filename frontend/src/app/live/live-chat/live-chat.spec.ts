import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LiveChatComponent } from './live-chat';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';
import { By } from '@angular/platform-browser';

describe('LiveChatComponent', () => {
  let component: LiveChatComponent;
  let fixture: ComponentFixture<LiveChatComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [LiveChatComponent],
      imports: [HttpClientTestingModule, FormsModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LiveChatComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should send message and add to messages', () => {
    component.newMessage = 'Olá!';
    fixture.detectChanges();

    component.sendMessage();

    const req = httpMock.expectOne('/live/chat');
    expect(req.request.method).toBe('POST');
    req.flush({ user: 'Henrique', text: 'Olá!', timestamp: '2025-08-26T18:01:00Z' });

    expect(component.messages.length).toBe(1);
    expect(component.messages[0].text).toBe('Olá!');
    expect(component.newMessage).toBe('');
    expect(component.sending).toBeFalse();
  });

  it('should show error message on backend error', () => {
    component.newMessage = 'Mensagem de erro';
    fixture.detectChanges();

    component.sendMessage();

    const req = httpMock.expectOne('/live/chat');
    req.error(new ErrorEvent('Network error'));

    expect(component.errorMsg).toBe('Erro ao enviar mensagem.');
    expect(component.sending).toBeFalse();
  });

  it('should disable button when sending or input is empty', () => {
    component.newMessage = '';
    fixture.detectChanges();
    const button = fixture.debugElement.query(By.css('button')).nativeElement;
    expect(button.disabled).toBeTrue();

    component.newMessage = 'Teste';
    component.sending = true;
    fixture.detectChanges();
    expect(button.disabled).toBeTrue();
  });
});