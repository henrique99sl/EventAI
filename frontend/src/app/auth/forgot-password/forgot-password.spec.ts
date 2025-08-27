import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { ForgotPasswordComponent } from './forgot-password';

describe('ForgotPasswordComponent', () => {
  let component: ForgotPasswordComponent;
  let fixture: ComponentFixture<ForgotPasswordComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ForgotPasswordComponent],
      imports: [FormsModule]
    }).compileComponents();

    fixture = TestBed.createComponent(ForgotPasswordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show error if email is missing', () => {
    component.email = '';
    component.onSubmit();
    expect(component.error).toBe('Por favor insira o seu email.');
  });

  it('should show error if email is not found', () => {
    component.email = 'naoexiste@email.com';
    component.onSubmit();
    expect(component.error).toBe('Email não encontrado!');
  });

  it('should show message if email exists', () => {
    component.email = 'existe@email.com';
    component.onSubmit();
    expect(component.message).toBe('Se o email estiver registado irá receber instruções de recuperação.');
  });
});