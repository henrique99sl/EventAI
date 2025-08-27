import { Component } from '@angular/core';

@Component({
  selector: 'app-register',
  templateUrl: './register.html',
  styleUrls: ['./register.scss']
})
export class RegisterComponent {
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  error: string = '';
  success: string = '';

  onRegister() {
    this.error = '';
    this.success = '';

    if (!this.email || !this.password || !this.confirmPassword) {
      this.error = 'Preencha todos os campos!';
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.error = 'As passwords não coincidem!';
      return;
    }

    // Simulação de registo, substitua pela chamada ao backend!
    if (this.email === 'demo@email.com') {
      this.error = 'Email já está registado!';
    } else {
      this.success = 'Registo efetuado com sucesso!';
      this.email = '';
      this.password = '';
      this.confirmPassword = '';
    }
  }
}