import { Component } from '@angular/core';
import { AssistantMessage } from './assistant-history/assistant-history';

@Component({
  selector: 'app-assistant',
  templateUrl: './assistant.component.html',
  styleUrls: ['./assistant.component.scss']
})
export class AssistantComponent {
  messages: AssistantMessage[] = [
    { id: 1, user: 'User', text: 'Olá!', timestamp: new Date() },
    { id: 2, user: 'Assistant', text: 'Oi, como posso ajudar?', timestamp: new Date() }
  ];

  addMessage(text: string) {
    this.messages.push({
      id: this.messages.length + 1,
      user: 'User',
      text,
      timestamp: new Date()
    });
    // Simulação de resposta do assistente
    setTimeout(() => {
      this.messages.push({
        id: this.messages.length + 1,
        user: 'Assistant',
        text: 'Recebi: ' + text,
        timestamp: new Date()
      });
    }, 700);
  }
}