import { Component } from '@angular/core';

export interface AgendaItem {
  time: string;
  title: string;
  speaker?: string;
}

@Component({
  selector: 'app-agenda',
  templateUrl: './agenda.html',
  styleUrls: ['./agenda.scss']
})
export class AgendaComponent {
  agenda: AgendaItem[] = [
    { time: '09:00', title: 'Welcome & Opening', speaker: 'Staff' },
    { time: '10:00', title: 'Keynote: The Future of Events', speaker: 'Dr. Alice' },
    { time: '11:30', title: 'Networking Break' },
    { time: '12:00', title: 'Panel Discussion: AI in Events', speaker: 'Panelists' }
  ];
}