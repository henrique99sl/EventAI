import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-assistant-chat',
  templateUrl: './assistant-chat.html',
  styleUrls: ['./assistant-chat.scss']
})
export class AssistantChatComponent {
  @Input() messages: { user: string, text: string, timestamp: Date }[] = [];
  @Output() sendMessage = new EventEmitter<string>();

  userInput = '';

  onSend() {
    const message = this.userInput.trim();
    if (message) {
      this.sendMessage.emit(message);
      this.userInput = '';
    }
  }
}