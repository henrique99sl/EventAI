import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AssistantHistoryComponent, AssistantMessage } from './assistant-history';
import { By } from '@angular/platform-browser';

describe('AssistantHistoryComponent', () => {
  let component: AssistantHistoryComponent;
  let fixture: ComponentFixture<AssistantHistoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AssistantHistoryComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AssistantHistoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show messages', () => {
    const messages: AssistantMessage[] = [
      { id: 1, user: 'User', text: 'Olá!', timestamp: new Date() },
      { id: 2, user: 'Assistant', text: 'Oi, como posso ajudar?', timestamp: new Date() }
    ];
    component.messages = messages;
    fixture.detectChanges();

    const msgEls = fixture.debugElement.queryAll(By.css('.message'));
    expect(msgEls.length).toBe(2);
    expect(msgEls[0].nativeElement.textContent).toContain('Olá!');
    expect(msgEls[1].nativeElement.textContent).toContain('Oi, como posso ajudar?');
  });

  it('should show empty state', () => {
    component.messages = [];
    fixture.detectChanges();

    const emptyEl = fixture.debugElement.query(By.css('.empty'));
    expect(emptyEl).toBeTruthy();
    expect(emptyEl.nativeElement.textContent).toContain('Nenhum histórico');
  });
});