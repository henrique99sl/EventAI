import { Component } from '@angular/core';

@Component({
  selector: 'app-social-login',
  templateUrl: './social-login.html',
  styleUrls: ['./social-login.scss']
})
export class SocialLoginComponent {

  onGoogleLogin() {
    // Aqui vai a lógica de login Google (redirecionar ou chamar serviço)
    window.location.href = '/api/auth/google'; // Exemplo de redirecionamento
  }

  onFacebookLogin() {
    // Aqui vai a lógica de login Facebook
    window.location.href = '/api/auth/facebook'; // Exemplo de redirecionamento
  }
}