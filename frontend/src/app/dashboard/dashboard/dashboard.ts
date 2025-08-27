import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class DashboardComponent {
  title = 'Dashboard';
  stats = [
    { name: 'Events', value: 12 },
    { name: 'Speakers', value: 7 },
    { name: 'Attendees', value: 230 }
  ];
}