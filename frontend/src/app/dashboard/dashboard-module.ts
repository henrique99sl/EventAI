import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DashboardComponent } from './dashboard/dashboard';
import { AssistantWidgetComponent } from './assistant-widget/assistant-widget';
import { FeedbackWidgetComponent } from './feedback-widget/feedback-widget';
import { NotificationsComponent } from './notifications/notifications';

@NgModule({
  declarations: [
    DashboardComponent,
    AssistantWidgetComponent,
    FeedbackWidgetComponent,
    NotificationsComponent
  ],
  imports: [
    CommonModule,
    FormsModule
  ],
  exports: [
    DashboardComponent,
    AssistantWidgetComponent,
    FeedbackWidgetComponent,
    NotificationsComponent
  ]
})
export class DashboardModule {}