import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { GamifiedFeedbackComponent } from './gamified-feedback';
import { By } from '@angular/platform-browser';

describe('GamifiedFeedbackComponent', () => {
  let component: GamifiedFeedbackComponent;
  let fixture: ComponentFixture<GamifiedFeedbackComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GamifiedFeedbackComponent],
      imports: [FormsModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GamifiedFeedbackComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should disable submit button if no emoji is selected', () => {
    component.selectedEmoji = null;
    fixture.detectChanges();
    const submitBtn = fixture.debugElement.query(By.css('button[type="submit"]'));
    expect(submitBtn.nativeElement.disabled).toBeTrue();
  });

  it('should emit feedbackSent event on send', () => {
    spyOn(component.feedbackSent, 'emit');
    component.selectedEmoji = '😍';
    component.comment = 'Muito bom!';
    fixture.detectChanges();

    const form = fixture.debugElement.query(By.css('form'));
    form.triggerEventHandler('ngSubmit', null);

    expect(component.feedbackSent.emit).toHaveBeenCalledWith({
      emoji: '😍',
      comment: 'Muito bom!'
    });
    expect(component.selectedEmoji).toBeNull();
    expect(component.comment).toBe('');
  });

  it('should highlight selected emoji', () => {
    component.selectedEmoji = '😞';
    fixture.detectChanges();
    const selectedEmojiBtn = fixture.debugElement.query(By.css('.emoji-group button.selected'));
    expect(selectedEmojiBtn).toBeTruthy();
    expect(selectedEmojiBtn.nativeElement.textContent).toContain('😞');
  });
});