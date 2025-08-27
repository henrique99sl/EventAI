import { Component, Input } from '@angular/core';

export interface CalendarEvent {
  id: number;
  title: string;
  date: string;
  time?: string;
  location?: string;
  description?: string;
}

@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.html',
  styleUrls: ['./calendar.scss']
})
export class CalendarComponent {
  @Input() events: CalendarEvent[] = [];
}