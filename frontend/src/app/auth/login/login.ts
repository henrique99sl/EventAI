import { Component } from '@angular/core';
import { Router } from '@angular/router'; // <-- Importa o Router

@Component({
  selector: 'app-login',
  templateUrl: './login.html',
  styleUrls: ['./login.scss']
})
export class LoginComponent {
  email: string = '';
  password: string = '';
  error: string = '';

  constructor(private router: Router) {} // <-- Injeta o Router

  onLogin() {
    if (!this.email || !this.password) {
      this.error = 'Preencha o email e a password!';
      return;
    }
    if (this.email === 'demo@email.com' && this.password === '123456') {
      this.error = '';
      this.router.navigate(['/dashboard']); // <-- Navega para dashboard!
    } else {
      this.error = 'Email ou password inválidos!';
    }
  }
}