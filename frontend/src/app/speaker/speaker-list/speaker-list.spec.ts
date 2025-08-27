import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SpeakerListComponent, SpeakerItem } from './speaker-list';

describe('SpeakerListComponent', () => {
  let component: SpeakerListComponent;
  let fixture: ComponentFixture<SpeakerListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SpeakerListComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpeakerListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show empty when no speakers', () => {
    component.speakers = [];
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.empty')?.textContent).toContain('Nenhum palestrante encontrado.');
  });

  it('should show speaker cards', () => {
    const speakers: SpeakerItem[] = [
      { id: 1, name: 'João Pedro', bio: 'Expert em Cloud', avatarUrl: 'joao.jpg', topics: ['Cloud', 'DevOps'], social: [{ type: 'LinkedIn', url: 'https://linkedin.com/in/joao' }] },
      { id: 2, name: 'Maria Lopes', topics: ['UX'], bio: 'Designer especialista.' }
    ];
    component.speakers = speakers;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelectorAll('.speaker-card').length).toBe(2);
    expect(compiled.textContent).toContain('João Pedro');
    expect(compiled.textContent).toContain('Expert em Cloud');
    expect(compiled.textContent).toContain('Cloud');
    expect(compiled.textContent).toContain('DevOps');
    expect(compiled.textContent).toContain('LinkedIn');
    expect(compiled.textContent).toContain('Maria Lopes');
    expect(compiled.textContent).toContain('Designer especialista.');
    expect(compiled.textContent).toContain('UX');
  });
});