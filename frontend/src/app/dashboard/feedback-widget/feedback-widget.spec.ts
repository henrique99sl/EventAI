import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FeedbackWidgetComponent } from './feedback-widget';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';
import { By } from '@angular/platform-browser';

describe('FeedbackWidgetComponent', () => {
  let component: FeedbackWidgetComponent;
  let fixture: ComponentFixture<FeedbackWidgetComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FeedbackWidgetComponent],
      imports: [HttpClientTestingModule, FormsModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FeedbackWidgetComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should submit feedback and show success message', () => {
    component.feedbackText = 'Ótimo evento!';
    fixture.detectChanges();

    component.submitFeedback();

    const req = httpMock.expectOne('/feedback');
    expect(req.request.method).toBe('POST');
    req.flush({});

    expect(component.successMsg).toBe('Obrigado pelo feedback!');
    expect(component.feedbackText).toBe('');
    expect(component.submitting).toBeFalse();
  });

  it('should show error message on backend error', () => {
    component.feedbackText = 'Teste erro';
    fixture.detectChanges();

    component.submitFeedback();

    const req = httpMock.expectOne('/feedback');
    req.error(new ErrorEvent('Network error'));

    expect(component.errorMsg).toContain('Erro ao enviar feedback');
    expect(component.submitting).toBeFalse();
  });

  it('should disable button when submitting or textarea is empty', () => {
    component.feedbackText = '';
    fixture.detectChanges();
    const button = fixture.debugElement.query(By.css('button')).nativeElement;
    expect(button.disabled).toBeTrue();

    component.feedbackText = 'Alguma coisa';
    component.submitting = true;
    fixture.detectChanges();
    expect(button.disabled).toBeTrue();
  });
});