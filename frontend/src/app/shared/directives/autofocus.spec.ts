import { AutofocusDirective } from './autofocus';
import { Component, DebugElement } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

@Component({
  template: `<input appAutofocus />`
})
class TestComponent {}

describe('AutofocusDirective', () => {
  let fixture: ComponentFixture<TestComponent>;
  let inputEl: DebugElement;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TestComponent, AutofocusDirective]
    });
    fixture = TestBed.createComponent(TestComponent);
    inputEl = fixture.debugElement.query(By.css('input'));
  });

  it('should focus the input element', () => {
    spyOn(inputEl.nativeElement, 'focus');
    fixture.detectChanges();
    expect(inputEl.nativeElement.focus).toHaveBeenCalled();
  });
});