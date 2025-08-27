import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface LiveStats {
  viewers: number;
  messages: number;
  votes: number;
  updatedAt: string;
}

@Component({
  selector: 'app-stats',
  templateUrl: './stats.html',
  styleUrls: ['./stats.scss']
})
export class StatsComponent implements OnInit {
  stats: LiveStats | null = null;
  loading = false;
  errorMsg = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.fetchStats();
  }

  fetchStats() {
    this.loading = true;
    this.errorMsg = '';
    this.http.get<LiveStats>('/live/stats').subscribe({
      next: (data) => {
        this.stats = data;
        this.loading = false;
      },
      error: () => {
        this.errorMsg = 'Erro ao carregar estatísticas.';
        this.loading = false;
      }
    });
  }
}