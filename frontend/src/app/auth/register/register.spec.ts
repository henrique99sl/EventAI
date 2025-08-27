import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { RegisterComponent } from './register';

describe('RegisterComponent', () => {
  let component: RegisterComponent;
  let fixture: ComponentFixture<RegisterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RegisterComponent],
      imports: [FormsModule]
    }).compileComponents();

    fixture = TestBed.createComponent(RegisterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show error if fields are missing', () => {
    component.email = '';
    component.password = '';
    component.confirmPassword = '';
    component.onRegister();
    expect(component.error).toBe('Preencha todos os campos!');
  });

  it('should show error if passwords do not match', () => {
    component.email = 'user@email.com';
    component.password = '123456';
    component.confirmPassword = '654321';
    component.onRegister();
    expect(component.error).toBe('As passwords não coincidem!');
  });

  it('should show error if email is already registered', () => {
    component.email = 'demo@email.com';
    component.password = '123456';
    component.confirmPassword = '123456';
    component.onRegister();
    expect(component.error).toBe('Email já está registado!');
  });

  it('should show success for valid registration', () => {
    component.email = 'novo@email.com';
    component.password = '123456';
    component.confirmPassword = '123456';
    component.onRegister();
    expect(component.success).toBe('Registo efetuado com sucesso!');
  });
});