import { ComponentFixture, TestBed } from '@angular/core/testing';
import { OrganizerModule } from './organizer-module';
import { OrganizerComponent } from './organizer.component';
import { By } from '@angular/platform-browser';

describe('OrganizerComponent', () => {
  let component: OrganizerComponent;
  let fixture: ComponentFixture<OrganizerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrganizerModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OrganizerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should add a new task', () => {
    component.newTaskTitle = 'Nova tarefa';
    component.addTask();
    fixture.detectChanges();

    expect(component.tasks.some(t => t.title === 'Nova tarefa')).toBeTrue();
  });

  it('should toggle task status', () => {
    const task = { id: 99, title: 'Teste', done: false };
    component.tasks = [task];
    component.toggleTask(task);
    expect(task.done).toBeTrue();
    component.toggleTask(task);
    expect(task.done).toBeFalse();
  });

  it('should remove a task', () => {
    const task1 = { id: 1, title: 'Um', done: false };
    const task2 = { id: 2, title: 'Dois', done: false };
    component.tasks = [task1, task2];
    component.removeTask(task1);
    expect(component.tasks.length).toBe(1);
    expect(component.tasks[0].title).toBe('Dois');
  });

  it('should show empty message when no tasks', () => {
    component.tasks = [];
    fixture.detectChanges();
    const emptyEl = fixture.debugElement.query(By.css('.empty'));
    expect(emptyEl).toBeTruthy();
    expect(emptyEl.nativeElement.textContent).toContain('Nenhuma tarefa');
  });
});