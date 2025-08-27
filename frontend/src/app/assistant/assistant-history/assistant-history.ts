import { Component, Input } from '@angular/core';

export interface AssistantMessage {
  id: number;
  user: string;
  text: string;
  timestamp: Date;
}

@Component({
  selector: 'app-assistant-history',
  templateUrl: './assistant-history.html',
  styleUrls: ['./assistant-history.scss']
})
export class AssistantHistoryComponent {
  @Input() messages: AssistantMessage[] = [];
}