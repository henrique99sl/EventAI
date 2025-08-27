import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ExportReportsComponent } from './export-reports';

describe('ExportReportsComponent', () => {
  let component: ExportReportsComponent;
  let fixture: ComponentFixture<ExportReportsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ExportReportsComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ExportReportsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should disable export button when no tasks', () => {
    component.tasks = [];
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const btn = compiled.querySelector('button');
    expect(btn?.disabled).toBeTrue();
  });

  it('should enable export button when tasks exist', () => {
    component.tasks = [
      { id: 1, title: 'Tarefa 1', done: true }
    ];
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const btn = compiled.querySelector('button');
    expect(btn?.disabled).toBeFalse();
  });

  it('should build CSV correctly', () => {
    component.tasks = [
      { id: 1, title: 'Teste', done: false }
    ];
    // Spy on link creation and click
    spyOn(document.body, 'appendChild');
    spyOn(document.body, 'removeChild');
    spyOn(URL, 'createObjectURL').and.returnValue('blob:url');
    spyOn(URL, 'revokeObjectURL');

    component.exportCSV();

    expect(document.body.appendChild).toHaveBeenCalled();
    expect(document.body.removeChild).toHaveBeenCalled();
    expect(URL.createObjectURL).toHaveBeenCalled();
    expect(URL.revokeObjectURL).toHaveBeenCalled();
  });
});