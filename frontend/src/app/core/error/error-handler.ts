import { ErrorHandler, Injectable } from '@angular/core';
import { ToastService } from './toast.service';

@Injectable()
export class AppErrorHandler implements ErrorHandler {
  constructor(private toastService: ToastService) {}

  handleError(error: any): void {
    // Log error to console (or external service)
    console.error('An error occurred:', error);

    // Show a toast notification to user
    this.toastService.show('An unexpected error occurred.', { type: 'error' });

    // Optionally rethrow or handle the error further
    // throw error;
  }
}