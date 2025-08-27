import { Component } from '@angular/core';

interface OrganizerTask {
  id: number;
  title: string;
  done: boolean;
}

@Component({
  selector: 'app-organizer',
  templateUrl: './organizer.component.html',
  styleUrls: ['./organizer.component.scss']
})
export class OrganizerComponent {
  tasks: OrganizerTask[] = [
    { id: 1, title: 'Primeira tarefa', done: false },
    { id: 2, title: 'Segunda tarefa', done: true }
  ];

  newTaskTitle = '';

  addTask() {
    const title = this.newTaskTitle.trim();
    if (title) {
      this.tasks.push({
        id: this.tasks.length + 1,
        title,
        done: false
      });
      this.newTaskTitle = '';
    }
  }

  toggleTask(task: OrganizerTask) {
    task.done = !task.done;
  }

  removeTask(task: OrganizerTask) {
    this.tasks = this.tasks.filter(t => t.id !== task.id);
  }
}