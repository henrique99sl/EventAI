import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { AssistantChatComponent } from './assistant-chat';
import { By } from '@angular/platform-browser';

describe('AssistantChatComponent', () => {
  let component: AssistantChatComponent;
  let fixture: ComponentFixture<AssistantChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AssistantChatComponent],
      imports: [FormsModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AssistantChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display messages', () => {
    component.messages = [
      { user: 'User', text: 'Oi', timestamp: new Date() },
      { user: 'Assistant', text: 'Olá! Como posso ajudar?', timestamp: new Date() }
    ];
    fixture.detectChanges();
    const msgEls = fixture.debugElement.queryAll(By.css('.message'));
    expect(msgEls.length).toBe(2);
    expect(msgEls[0].nativeElement.textContent).toContain('Oi');
    expect(msgEls[1].nativeElement.textContent).toContain('Olá! Como posso ajudar?');
  });

  it('should emit sendMessage event on send', () => {
    spyOn(component.sendMessage, 'emit');
    component.userInput = 'Teste';
    fixture.detectChanges();

    const form = fixture.debugElement.query(By.css('form'));
    form.triggerEventHandler('ngSubmit', null);

    expect(component.sendMessage.emit).toHaveBeenCalledWith('Teste');
    expect(component.userInput).toBe('');
  });

  it('should disable send button if input is empty', () => {
    component.userInput = '';
    fixture.detectChanges();
    const button = fixture.debugElement.query(By.css('button'));
    expect(button.nativeElement.disabled).toBeTrue();
  });
});