import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { FeedbackFormComponent } from './feedback-form';
import { By } from '@angular/platform-browser';

describe('FeedbackFormComponent', () => {
  let component: FeedbackFormComponent;
  let fixture: ComponentFixture<FeedbackFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FeedbackFormComponent],
      imports: [FormsModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FeedbackFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should disable submit button if feedback is empty', () => {
    component.feedbackText = '';
    fixture.detectChanges();
    const button = fixture.debugElement.query(By.css('button'));
    expect(button.nativeElement.disabled).toBeTrue();
  });

  it('should emit feedbackSubmitted event on submit', () => {
    spyOn(component.feedbackSubmitted, 'emit');
    component.feedbackText = 'Ótimo serviço!';
    component.rating = 5;
    fixture.detectChanges();

    const form = fixture.debugElement.query(By.css('form'));
    form.triggerEventHandler('ngSubmit', null);

    expect(component.feedbackSubmitted.emit).toHaveBeenCalledWith({
      feedback: 'Ótimo serviço!',
      rating: 5
    });
    expect(component.feedbackText).toBe('');
    expect(component.rating).toBeNull();
  });
});