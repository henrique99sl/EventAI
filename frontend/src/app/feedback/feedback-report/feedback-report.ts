import { Component, Input } from '@angular/core';

export interface FeedbackEntry {
  id: number;
  feedback: string;
  rating?: number;
  emoji?: string;
  comment?: string;
  date: Date;
}

@Component({
  selector: 'app-feedback-report',
  templateUrl: './feedback-report.html',
  styleUrls: ['./feedback-report.scss']
})
export class FeedbackReportComponent {
  @Input() feedbacks: FeedbackEntry[] = [];
}