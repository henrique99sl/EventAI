import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from './login';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [LoginComponent],
      imports: [FormsModule]
    }).compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show error if email or password is empty', () => {
    component.email = '';
    component.password = '';
    component.onLogin();
    expect(component.error).toBe('Preencha o email e a password!');
  });

  it('should show error for wrong credentials', () => {
    component.email = 'wrong@email.com';
    component.password = 'wrongpass';
    component.onLogin();
    expect(component.error).toBe('Email ou password inválidos!');
  });

  it('should not show error for correct credentials', () => {
    component.email = 'demo@email.com';
    component.password = '123456';
    component.onLogin();
    expect(component.error).toBe('');
  });
});