import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FeedbackReportComponent, FeedbackEntry } from './feedback-report';
import { By } from '@angular/platform-browser';

describe('FeedbackReportComponent', () => {
  let component: FeedbackReportComponent;
  let fixture: ComponentFixture<FeedbackReportComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FeedbackReportComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FeedbackReportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show empty message when no feedbacks', () => {
    component.feedbacks = [];
    fixture.detectChanges();
    const emptyEl = fixture.debugElement.query(By.css('.empty'));
    expect(emptyEl).toBeTruthy();
    expect(emptyEl.nativeElement.textContent).toContain('Nenhum feedback');
  });

  it('should show feedback entries in table', () => {
    const feedbacks: FeedbackEntry[] = [
      { id: 1, feedback: 'Ótimo!', rating: 5, emoji: '😍', comment: 'Muito bom', date: new Date() },
      { id: 2, feedback: 'Ruim', rating: 2, emoji: '😞', comment: '', date: new Date() }
    ];
    component.feedbacks = feedbacks;
    fixture.detectChanges();

    const rows = fixture.debugElement.queryAll(By.css('tbody tr'));
    expect(rows.length).toBe(2);
    expect(rows[0].nativeElement.textContent).toContain('Ótimo!');
    expect(rows[0].nativeElement.textContent).toContain('5');
    expect(rows[0].nativeElement.textContent).toContain('😍');
    expect(rows[1].nativeElement.textContent).toContain('Ruim');
    expect(rows[1].nativeElement.textContent).toContain('2');
    expect(rows[1].nativeElement.textContent).toContain('😞');
  });
});