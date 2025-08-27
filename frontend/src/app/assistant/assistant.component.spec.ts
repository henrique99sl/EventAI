import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AssistantComponent } from './assistant.component';
import { AssistantChatComponent } from './assistant-chat/assistant-chat';
import { AssistantHistoryComponent } from './assistant-history/assistant-history';
import { FormsModule } from '@angular/forms';

describe('AssistantComponent', () => {
  let component: AssistantComponent;
  let fixture: ComponentFixture<AssistantComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [
        AssistantComponent,
        AssistantChatComponent,
        AssistantHistoryComponent
      ],
      imports: [FormsModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AssistantComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should add user message and assistant reply', (done) => {
    const initLength = component.messages.length;
    component.addMessage('Teste');
    expect(component.messages.length).toBe(initLength + 1);
    expect(component.messages[component.messages.length - 1].user).toBe('User');
    setTimeout(() => {
      expect(component.messages.length).toBe(initLength + 2);
      expect(component.messages[component.messages.length - 1].user).toBe('Assistant');
      expect(component.messages[component.messages.length - 1].text).toContain('Recebi:');
      done();
    }, 800);
  });
});