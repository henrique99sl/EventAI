import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'dateFormat'
})
export class DateFormatPipe implements PipeTransform {
  transform(value: string | Date | null | undefined, format: string = 'shortDate'): string {
    if (!value) return '';
    const date = typeof value === 'string' ? new Date(value) : value;
    // Use Intl.DateTimeFormat para formatação básica
    if (format === 'shortDate') {
      return new Intl.DateTimeFormat('pt-BR').format(date);
    }
    if (format === 'longDate') {
      return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'full' }).format(date);
    }
    // Outros formatos
    return date.toLocaleString();
  }
}