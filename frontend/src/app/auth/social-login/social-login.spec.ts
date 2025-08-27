import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SocialLoginComponent } from './social-login';

describe('SocialLoginComponent', () => {
  let component: SocialLoginComponent;
  let fixture: ComponentFixture<SocialLoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SocialLoginComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(SocialLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have onGoogleLogin method', () => {
    expect(typeof component.onGoogleLogin).toBe('function');
  });

  it('should have onFacebookLogin method', () => {
    expect(typeof component.onFacebookLogin).toBe('function');
  });
});