import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface VoteOption {
  id: number;
  label: string;
  votes: number;
}

@Component({
  selector: 'app-voting',
  templateUrl: './voting.html',
  styleUrls: ['./voting.scss']
})
export class VotingComponent {
  options: VoteOption[] = [];
  selectedOptionId: number | null = null;
  submitting = false;
  successMsg = '';
  errorMsg = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadOptions();
  }

  loadOptions() {
    this.http.get<VoteOption[]>('/live/voting/options').subscribe({
      next: (opts) => {
        this.options = opts;
      },
      error: () => {
        this.errorMsg = 'Erro ao carregar opções de voto.';
      }
    });
  }

  vote() {
    if (this.selectedOptionId === null) return;
    this.submitting = true;
    this.successMsg = '';
    this.errorMsg = '';

    this.http.post('/live/voting/vote', { optionId: this.selectedOptionId }).subscribe({
      next: () => {
        this.successMsg = 'Voto registado!';
        this.submitting = false;
        this.loadOptions();
      },
      error: () => {
        this.errorMsg = 'Erro ao enviar voto.';
        this.submitting = false;
      }
    });
  }
}