import { Component, Input } from '@angular/core';

export interface EventItem {
  id: number;
  title: string;
  date: string;
  time?: string;
  location?: string;
  description?: string;
}

@Component({
  selector: 'app-event-list',
  templateUrl: './event-list.html',
  styleUrls: ['./event-list.scss']
})
export class EventListComponent {
  @Input() events: EventItem[] = [];
}