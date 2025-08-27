import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SpeakerProfileComponent, SpeakerProfile } from './profile';

describe('SpeakerProfileComponent', () => {
  let component: SpeakerProfileComponent;
  let fixture: ComponentFixture<SpeakerProfileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SpeakerProfileComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpeakerProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show empty message when no profile', () => {
    component.profile = undefined as any;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.empty')?.textContent).toContain('Nenhum perfil encontrado.');
  });

  it('should show speaker profile data', () => {
    const profile: SpeakerProfile = {
      id: 1,
      name: 'Ana Silva',
      bio: 'Especialista em IA',
      avatarUrl: 'ana.jpg',
      topics: ['Inteligência Artificial', 'Machine Learning'],
      social: [{ type: 'LinkedIn', url: 'https://linkedin.com/in/ana' }]
    };
    component.profile = profile;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Ana Silva');
    expect(compiled.textContent).toContain('Especialista em IA');
    expect(compiled.textContent).toContain('Inteligência Artificial');
    expect(compiled.textContent).toContain('Machine Learning');
    expect(compiled.textContent).toContain('LinkedIn');
  });
});