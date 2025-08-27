import { Injectable } from '@angular/core';

export interface ToastOptions {
  type?: 'success' | 'error' | 'info' | 'warning';
  duration?: number; // in ms
}

@Injectable({
  providedIn: 'root'
})
export class ToastService {
  show(message: string, options: ToastOptions = {}): void {
    const type = options.type ?? 'info';
    const duration = options.duration ?? 3000;
    console.log(`[${type.toUpperCase()}] ${message} (duration: ${duration}ms)`);
    // Implemente o toast de verdade aqui se quiser!
  }
}