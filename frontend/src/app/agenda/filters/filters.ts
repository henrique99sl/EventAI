import { Component, Output, EventEmitter, Input } from '@angular/core';

export interface FilterOptions {
  date?: string;
  location?: string;
  search?: string;
}

@Component({
  selector: 'app-filters',
  templateUrl: './filters.html',
  styleUrls: ['./filters.scss']
})
export class FiltersComponent {
  @Input() initialFilters: FilterOptions = {};
  @Output() filtersChanged = new EventEmitter<FilterOptions>();

  filters: FilterOptions = {};

  ngOnInit() {
    this.filters = { ...this.initialFilters };
  }

  applyFilters() {
    this.filtersChanged.emit({ ...this.filters });
  }

  clearFilters() {
    this.filters = {};
    this.applyFilters();
  }
}