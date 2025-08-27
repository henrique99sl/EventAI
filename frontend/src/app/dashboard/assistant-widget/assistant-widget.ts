import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-assistant-widget',
  templateUrl: './assistant-widget.html',
  styleUrls: ['./assistant-widget.scss']
})
export class AssistantWidgetComponent {
  userMessage = '';
  conversation: { from: 'user' | 'assistant', message: string }[] = [];
  loading = false;

  constructor(private http: HttpClient) {}

  sendMessage() {
    const message = this.userMessage.trim();
    if (!message) return;

    this.conversation.push({ from: 'user', message });
    this.loading = true;

    this.http.post<{ reply: string }>('/assistant', { message }).subscribe({
      next: data => {
        this.conversation.push({ from: 'assistant', message: data.reply });
        this.loading = false;
        this.userMessage = '';
      },
      error: () => {
        this.conversation.push({ from: 'assistant', message: 'Erro ao contactar o assistente.' });
        this.loading = false;
      }
    });
  }
}