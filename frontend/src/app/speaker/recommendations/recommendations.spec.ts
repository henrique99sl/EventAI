import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SpeakerRecommendationsComponent, SpeakerRecommendation } from './recommendations';

describe('SpeakerRecommendationsComponent', () => {
  let component: SpeakerRecommendationsComponent;
  let fixture: ComponentFixture<SpeakerRecommendationsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SpeakerRecommendationsComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpeakerRecommendationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show empty when no recommendations', () => {
    component.recommendations = [];
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.empty')?.textContent).toContain('Nenhuma recomendação disponível.');
  });

  it('should show recommendation cards', () => {
    const recommendations: SpeakerRecommendation[] = [
      { id: 1, name: 'João Pedro', bio: 'Expert em Cloud', avatarUrl: 'joao.jpg', topics: ['Cloud', 'DevOps'], reason: 'Participa em grandes eventos.' },
      { id: 2, name: 'Maria Lopes', topics: ['UX'], reason: 'Ótima comunicação.' }
    ];
    component.recommendations = recommendations;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelectorAll('.card').length).toBe(2);
    expect(compiled.textContent).toContain('João Pedro');
    expect(compiled.textContent).toContain('Expert em Cloud');
    expect(compiled.textContent).toContain('Cloud');
    expect(compiled.textContent).toContain('DevOps');
    expect(compiled.textContent).toContain('Participa em grandes eventos.');
    expect(compiled.textContent).toContain('Maria Lopes');
    expect(compiled.textContent).toContain('Ótima comunicação.');
    expect(compiled.textContent).toContain('UX');
  });
});