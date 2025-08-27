import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface Message {
  user: string;
  text: string;
  timestamp: string;
}

@Component({
  selector: 'app-live-chat',
  templateUrl: './live-chat.html',
  styleUrls: ['./live-chat.scss']
})
export class LiveChatComponent {
  messages: Message[] = [];
  newMessage = '';
  sending = false;
  errorMsg = '';

  constructor(private http: HttpClient) {}

  sendMessage() {
    const text = this.newMessage.trim();
    if (!text) return;

    this.sending = true;
    this.errorMsg = '';

    this.http.post<Message>('/live/chat', { text }).subscribe({
      next: (msg) => {
        this.messages.push(msg);
        this.newMessage = '';
        this.sending = false;
      },
      error: () => {
        this.errorMsg = 'Erro ao enviar mensagem.';
        this.sending = false;
      }
    });
  }
}