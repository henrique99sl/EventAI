import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.html',
  styleUrls: ['./landing.scss']
})
export class LandingComponent {
  constructor(private router: Router) {}
  goToApp() {
    this.router.navigate(['/dashboard']); // ou '/app'
  }
}