import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// Import shared modules if needed
// import { MaterialModule } from '../shared/material/material.module';

// Import all speaker components
import { SpeakerComponent } from './speaker.component';
import { SpeakerProfileComponent } from './profile/profile';
import { SpeakerRecommendationsComponent } from './recommendations/recommendations';
import { SpeakerListComponent } from './speaker-list/speaker-list';

@NgModule({
  declarations: [
    SpeakerComponent,
    SpeakerProfileComponent,
    SpeakerRecommendationsComponent,
    SpeakerListComponent
  ],
  imports: [
    CommonModule,
    // MaterialModule,
    // Add FormsModule or other modules if needed
  ],
  exports: [
    SpeakerComponent,
    SpeakerProfileComponent,
    SpeakerRecommendationsComponent,
    SpeakerListComponent
  ]
})
export class SpeakerModule { }