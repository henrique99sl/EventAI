import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-feedback-form',
  templateUrl: './feedback-form.html',
  styleUrls: ['./feedback-form.scss']
})
export class FeedbackFormComponent {
  feedbackText = '';
  rating: number | null = null;

  @Output() feedbackSubmitted = new EventEmitter<{ feedback: string, rating: number | null }>();

  submitFeedback() {
    if (this.feedbackText.trim()) {
      this.feedbackSubmitted.emit({
        feedback: this.feedbackText,
        rating: this.rating
      });
      this.feedbackText = '';
      this.rating = null;
    }
  }
}