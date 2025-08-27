import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FeedbackComponent } from './feedback.component';
import { FeedbackFormComponent } from './feedback-form/feedback-form';
import { FeedbackReportComponent } from './feedback-report/feedback-report';
import { GamifiedFeedbackComponent } from './gamified-feedback/gamified-feedback';

@NgModule({
  declarations: [
    FeedbackComponent,
    FeedbackFormComponent,
    FeedbackReportComponent,
    GamifiedFeedbackComponent
  ],
  imports: [CommonModule, FormsModule],
  exports: [
    FeedbackComponent,
    FeedbackFormComponent,
    FeedbackReportComponent,
    GamifiedFeedbackComponent
  ]
})
export class FeedbackModule {}