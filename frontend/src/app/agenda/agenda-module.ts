import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AgendaComponent } from './agenda.component';
import { FiltersComponent } from './filters/filters';

@NgModule({
  declarations: [
    AgendaComponent,
    FiltersComponent
  ],
  imports: [CommonModule, FormsModule],
  exports: [
    AgendaComponent,
    FiltersComponent
  ]
})
export class AgendaModule {}