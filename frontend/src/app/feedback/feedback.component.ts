import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-feedback',
  templateUrl: './feedback.component.html',
  styleUrls: ['./feedback.component.scss']
})
export class FeedbackComponent {
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