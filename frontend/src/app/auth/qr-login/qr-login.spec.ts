import { ComponentFixture, TestBed } from '@angular/core/testing';
import { QrLoginComponent } from './qr-login';

describe('QrLoginComponent', () => {
  let component: QrLoginComponent;
  let fixture: ComponentFixture<QrLoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [QrLoginComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(QrLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set qrCodeUrl on init', () => {
    component.ngOnInit();
    expect(component.qrCodeUrl).toContain('qrserver.com');
  });

  it('should simulate scan success', () => {
    component.onScanSuccess();
    expect(component.scanned).toBeTrue();
    expect(component.message).toBe('Login efetuado com sucesso via QR!');
    expect(component.error).toBe('');
  });

  it('should simulate scan error', () => {
    component.onScanError();
    expect(component.error).toBe('Falha ao ler QR code!');
    expect(component.message).toBe('');
    expect(component.scanned).toBeFalse();
  });
});