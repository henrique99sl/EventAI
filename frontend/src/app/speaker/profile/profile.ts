import { Component, Input } from '@angular/core';

export interface SpeakerProfile {
  id: number;
  name: string;
  bio?: string;
  avatarUrl?: string;
  topics?: string[];
  social?: { type: string; url: string }[];
}

@Component({
  selector: 'app-speaker-profile',
  templateUrl: './profile.html',
  styleUrls: ['./profile.scss']
})
export class SpeakerProfileComponent {
  @Input() profile!: SpeakerProfile;
}