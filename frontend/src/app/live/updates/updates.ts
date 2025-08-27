import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface LiveUpdate {
  id: number;
  message: string;
  timestamp: string;
  type?: string;
}

@Component({
  selector: 'app-updates',
  templateUrl: './updates.html',
  styleUrls: ['./updates.scss']
})
export class UpdatesComponent implements OnInit {
  updates: LiveUpdate[] = [];
  loading = false;
  errorMsg = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadUpdates();
  }

  loadUpdates() {
    this.loading = true;
    this.errorMsg = '';
    this.http.get<LiveUpdate[]>('/live/updates').subscribe({
      next: (data) => {
        this.updates = data;
        this.loading = false;
      },
      error: () => {
        this.errorMsg = 'Erro ao carregar atualizações.';
        this.loading = false;
      }
    });
  }
}