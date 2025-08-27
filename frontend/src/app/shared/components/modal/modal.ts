import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-modal',
  template: `
    <div class="app-modal-backdrop" (click)="close()"></div>
    <div class="app-modal">
      <button class="app-modal-close" (click)="close()">&times;</button>
      <ng-content></ng-content>
    </div>
  `,
  styleUrls: ['./modal.scss']
})
export class ModalComponent {
  @Input() visible = false;
  @Output() closed = new EventEmitter<void>();

  close() {
    this.closed.emit();
  }
}