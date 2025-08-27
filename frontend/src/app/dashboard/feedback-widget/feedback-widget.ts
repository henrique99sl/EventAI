import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-feedback-widget',
  templateUrl: './feedback-widget.html',
  styleUrls: ['./feedback-widget.scss']
})
export class FeedbackWidgetComponent {
  feedbackText = '';
  submitting = false;
  successMsg = '';
  errorMsg = '';

  constructor(private http: HttpClient) {}

  submitFeedback() {
    const text = this.feedbackText.trim();
    if (!text) return;

    this.submitting = true;
    this.successMsg = '';
    this.errorMsg = '';

    this.http.post('/feedback', { feedback: text }).subscribe({
      next: () => {
        this.successMsg = 'Obrigado pelo feedback!';
        this.feedbackText = '';
        this.submitting = false;
      },
      error: () => {
        this.errorMsg = 'Erro ao enviar feedback. Tenta novamente.';
        this.submitting = false;
      }
    });
  }
}