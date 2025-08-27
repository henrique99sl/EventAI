import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-input',
  template: `
    <input
      [type]="type"
      [placeholder]="placeholder"
      [value]="value"
      [disabled]="disabled"
      (input)="onInput($event)"
      class="app-input"
    />
  `,
  styleUrls: ['./input.scss']
})
export class InputComponent {
  @Input() type: string = 'text';
  @Input() placeholder: string = '';
  @Input() value: string = '';
  @Input() disabled = false;

  onInput(event: Event) {
    // Custom input logic can be added here if needed
  }
}