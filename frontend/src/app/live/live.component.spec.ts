import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LiveComponent } from './live.component';
import { LiveModule } from './live-module';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('LiveComponent', () => {
  let component: LiveComponent;
  let fixture: ComponentFixture<LiveComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LiveModule, HttpClientTestingModule]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LiveComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('deve criar o componente', () => {
    expect(component).toBeTruthy();
  });
});