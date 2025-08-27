import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FiltersComponent, FilterOptions } from './filters';
import { FormsModule } from '@angular/forms';
import { By } from '@angular/platform-browser';

describe('FiltersComponent', () => {
  let component: FiltersComponent;
  let fixture: ComponentFixture<FiltersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FiltersComponent],
      imports: [FormsModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FiltersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should emit filters on apply', () => {
    spyOn(component.filtersChanged, 'emit');
    component.filters = { date: '2025-09-01', location: 'Lisboa', search: 'evento' };
    component.applyFilters();
    expect(component.filtersChanged.emit).toHaveBeenCalledWith({
      date: '2025-09-01',
      location: 'Lisboa',
      search: 'evento'
    });
  });

  it('should clear filters', () => {
    component.filters = { date: '2025-09-01', location: 'Lisboa', search: 'evento' };
    spyOn(component.filtersChanged, 'emit');
    component.clearFilters();
    expect(component.filters).toEqual({});
    expect(component.filtersChanged.emit).toHaveBeenCalledWith({});
  });

  it('should set initial filters on ngOnInit', () => {
    component.initialFilters = { date: '2025-08-27', location: 'Porto' };
    component.ngOnInit();
    expect(component.filters).toEqual({ date: '2025-08-27', location: 'Porto' });
  });
});