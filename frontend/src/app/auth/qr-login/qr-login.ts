import { Component } from '@angular/core';

@Component({
  selector: 'app-qr-login',
  templateUrl: './qr-login.html',
  styleUrls: ['./qr-login.scss']
})
export class QrLoginComponent {
  qrCodeUrl: string = '';
  scanned: boolean = false;
  message: string = '';
  error: string = '';

  ngOnInit() {
    // Simulação: URL do QR gerado pelo backend
    this.qrCodeUrl = 'https://api.qrserver.com/v1/create-qr-code/?data=login-token-demo&size=180x180';
  }

  onScanSuccess() {
    // Simulação: O utilizador fez scan ao QR
    this.scanned = true;
    this.message = 'Login efetuado com sucesso via QR!';
    this.error = '';
  }

  onScanError() {
    this.error = 'Falha ao ler QR code!';
    this.message = '';
    this.scanned = false;
  }
}