import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-card',
  template: `
    <div class="app-card" [class.highlight]="highlight">
      <ng-content></ng-content>
    </div>
  `,
  styleUrls: ['./card.scss']
})
export class CardComponent {
  @Input() highlight = false;
}