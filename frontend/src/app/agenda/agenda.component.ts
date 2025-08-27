import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface Event {
  id: number;
  title: string;
  date: string;
  time?: string;
  location?: string;
  description?: string;
}

@Component({
  selector: 'app-agenda',
  templateUrl: './agenda.component.html',
  styleUrls: ['./agenda.component.scss']
})
export class AgendaComponent implements OnInit {
  events: Event[] = [];
  loading = false;
  errorMsg = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadEvents();
  }

  loadEvents() {
    this.loading = true;
    this.errorMsg = '';
    this.http.get<Event[]>('/events/calendar').subscribe({
      next: events => {
        this.events = events;
        this.loading = false;
      },
      error: () => {
        this.errorMsg = 'Erro ao carregar agenda.';
        this.loading = false;
      }
    });
  }
}