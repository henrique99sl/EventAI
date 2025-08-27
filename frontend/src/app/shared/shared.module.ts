import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// Import shared components, pipes, and directives here
// import { ButtonComponent } from './shared/components/button/button';
// import { DateFormatPipe } from './shared/pipes/date-format-pipe';
// import { AutofocusDirective } from './shared/directives/autofocus';

@NgModule({
  declarations: [
    // ButtonComponent,
    // DateFormatPipe,
    // AutofocusDirective,
    // ... add other shared components/pipes/directives here
  ],
  imports: [
    CommonModule
    // Add other modules like FormsModule, MaterialModule if needed
  ],
  exports: [
    // ButtonComponent,
    // DateFormatPipe,
    // AutofocusDirective,
    CommonModule
    // Add shared modules you want to export
  ]
})
export class SharedModule { }