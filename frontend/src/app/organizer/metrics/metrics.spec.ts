import { ComponentFixture, TestBed } from '@angular/core/testing';
import { OrganizerModule } from '../organizer-module';
import { MetricsComponent } from './metrics';

describe('MetricsComponent', () => {
  let fixture: ComponentFixture<MetricsComponent>;
  let component: MetricsComponent;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrganizerModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MetricsComponent);
    component = fixture.componentInstance;
    // Reset tasks before each test for isolation
    component.tasks = [];
    fixture.detectChanges();
  });

  it('deve criar o componente', () => {
    expect(component).toBeTruthy();
  });

  it('deve mostrar métricas zeradas sem tarefas', () => {
    component.tasks = [];
    fixture.detectChanges();
    expect(component.totalTasks).toBe(0);
    expect(component.completedTasks).toBe(0);
    expect(component.completionRate).toBe(0);
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.empty')?.textContent).toContain('Nenhuma tarefa');
  });

  it('deve calcular métricas corretamente', () => {
    component.tasks = [
      { done: true },
      { done: false },
      { done: true }
    ];
    fixture.detectChanges();
    expect(component.totalTasks).toBe(3);
    expect(component.completedTasks).toBe(2);
    expect(component.completionRate).toBe(67); // arredondado
  });

  it('deve mostrar mensagem de vazio quando não há tarefas', () => {
    component.tasks = [];
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.empty')?.textContent).toContain('Nenhuma tarefa');
  });
});