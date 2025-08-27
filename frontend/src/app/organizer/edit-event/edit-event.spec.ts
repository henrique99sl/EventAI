import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { EditEventComponent, EventData } from './edit-event';
import { By } from '@angular/platform-browser';

describe('EditEventComponent', () => {
  let component: EditEventComponent;
  let fixture: ComponentFixture<EditEventComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EditEventComponent],
      imports: [FormsModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EditEventComponent);
    component = fixture.componentInstance;
    component.event = {
      id: 1,
      title: 'Teste',
      date: '2025-08-27',
      location: 'Lisboa',
      description: 'Descrição teste'
    };
    fixture.detectChanges();
  });

  it('deve criar o componente', () => {
    expect(component).toBeTruthy();
  });

  it('deve emitir saveEvent com os dados corretos', () => {
    spyOn(component.saveEvent, 'emit');
    component.event.title = 'Novo título';
    component.onSave();
    expect(component.saveEvent.emit).toHaveBeenCalledWith(jasmine.objectContaining({
      title: 'Novo título'
    }));
  });

  it('deve emitir cancelEdit ao clicar cancelar', () => {
    spyOn(component.cancelEdit, 'emit');
    component.onCancel();
    expect(component.cancelEdit.emit).toHaveBeenCalled();
  });

  it('deve atualizar o campo título do evento via formulário', () => {
    // Obtém o input ligado ao ngModel do título
    const input = fixture.debugElement.query(By.css('input[name="title"]')).nativeElement;
    input.value = 'Alterado pelo teste';
    input.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    // Valida que o model está atualizado
    expect(component.event.title).toBe('Alterado pelo teste');

    // Cast necessário para obter o valor do input
    const compiled = fixture.nativeElement as HTMLElement;
    expect((compiled.querySelector('input[name="title"]') as HTMLInputElement)?.value).toBe('Alterado pelo teste');
  });
});