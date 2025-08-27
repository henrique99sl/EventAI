import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-button',
  template: `
    <button [type]="type" [disabled]="disabled" (click)="onClick($event)" class="app-button">
      <ng-content></ng-content>
    </button>
  `,
  styleUrls: ['./button.scss']
})
export class ButtonComponent {
  @Input() type: 'button' | 'submit' | 'reset' = 'button';
  @Input() disabled = false;

  onClick(event: Event) {
    // Custom click logic can be added here if needed
  }
}