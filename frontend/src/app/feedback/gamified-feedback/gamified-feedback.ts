import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-gamified-feedback',
  templateUrl: './gamified-feedback.html',
  styleUrls: ['./gamified-feedback.scss']
})
export class GamifiedFeedbackComponent {
  selectedEmoji: string | null = null;
  comment: string = '';

  @Output() feedbackSent = new EventEmitter<{emoji: string | null, comment: string}>();

  emojis = [
    { value: '😡', label: 'Muito ruim' },
    { value: '😞', label: 'Ruim' },
    { value: '😐', label: 'Neutro' },
    { value: '😊', label: 'Bom' },
    { value: '😍', label: 'Excelente' }
  ];

  sendFeedback() {
    if (this.selectedEmoji) {
      this.feedbackSent.emit({
        emoji: this.selectedEmoji,
        comment: this.comment
      });
      this.selectedEmoji = null;
      this.comment = '';
    }
  }
}