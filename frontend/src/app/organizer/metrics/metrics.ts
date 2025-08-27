import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-metrics',
  templateUrl: './metrics.html',
  styleUrls: ['./metrics.scss']
})
export class MetricsComponent {
  @Input() tasks: { done: boolean }[] = [];

  get totalTasks(): number {
    return this.tasks.length;
  }

  get completedTasks(): number {
    return this.tasks.filter(t => t.done).length;
  }

  get completionRate(): number {
    return this.totalTasks === 0 ? 0 : Math.round((this.completedTasks / this.totalTasks) * 100);
  }
}