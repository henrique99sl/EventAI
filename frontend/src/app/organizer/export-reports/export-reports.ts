import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-export-reports',
  templateUrl: './export-reports.html',
  styleUrls: ['./export-reports.scss']
})
export class ExportReportsComponent {
  @Input() tasks: { id: number; title: string; done: boolean }[] = [];

  exportCSV() {
    if (!this.tasks.length) return;

    const header = ['ID', 'Título', 'Concluída'];
    const rows = this.tasks.map(task => [
      task.id,
      `"${task.title.replace(/"/g, '""')}"`,
      task.done ? 'Sim' : 'Não'
    ]);
    const csvContent =
      [header, ...rows]
        .map(e => e.join(','))
        .join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'relatorio-tarefas.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
}