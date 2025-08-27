import { Component } from '@angular/core';

export interface Notification {
  id: number;
  message: string;
  type?: 'info' | 'success' | 'warning' | 'error';
  read?: boolean;
}

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.html',
  styleUrls: ['./notifications.scss']
})
export class NotificationsComponent {
  notifications: Notification[] = [
    { id: 1, message: 'Welcome to the event!', type: 'success', read: false },
    { id: 2, message: 'Your session starts in 15 minutes.', type: 'info', read: false },
    { id: 3, message: 'Feedback submitted successfully.', type: 'success', read: true }
  ];

  markAsRead(id: number): void {
    const found = this.notifications.find(n => n.id === id);
    if (found) {
      found.read = true;
    }
  }
}