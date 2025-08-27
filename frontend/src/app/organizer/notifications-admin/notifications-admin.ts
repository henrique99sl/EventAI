import { Component } from '@angular/core';

interface Notification {
  id: number;
  message: string;
  read: boolean;
  createdAt: Date;
}

@Component({
  selector: 'app-notifications-admin',
  templateUrl: './notifications-admin.html',
  styleUrls: ['./notifications-admin.scss']
})
export class NotificationsAdminComponent {
  notifications: Notification[] = [
    {
      id: 1,
      message: 'Nova tarefa adicionada!',
      read: false,
      createdAt: new Date()
    },
    {
      id: 2,
      message: 'Relatório exportado com sucesso.',
      read: true,
      createdAt: new Date(Date.now() - 1000 * 60 * 30)
    }
  ];

  markAsRead(notification: Notification) {
    notification.read = true;
  }

  removeNotification(notification: Notification) {
    this.notifications = this.notifications.filter(n => n.id !== notification.id);
  }
}