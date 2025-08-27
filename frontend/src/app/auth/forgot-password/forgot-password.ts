import { Component } from '@angular/core';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.html',
  styleUrls: ['./forgot-password.scss']
})
export class ForgotPasswordComponent {
  email: string = '';
  message: string = '';
  error: string = '';

  onSubmit() {
    this.error = '';
    this.message = '';
    if (!this.email) {
      this.error = 'Por favor insira o seu email.';
      return;
    }
    // Simulação de envio para backend
    if (this.email === 'naoexiste@email.com') {
      this.error = 'Email não encontrado!';
    } else {
      this.message = 'Se o email estiver registado irá receber instruções de recuperação.';
      this.email = '';
    }
  }
}