import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-loader',
  template: `
    <div class="app-loader" [class.inline]="inline">
      <span *ngIf="text">{{text}}</span>
      <div class="spinner"></div>
    </div>
  `,
  styleUrls: ['./loader.scss']
})
export class LoaderComponent {
  @Input() text?: string;
  @Input() inline = false;
}