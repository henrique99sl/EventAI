import { Component, Input } from '@angular/core';

export interface Speaker {
  id: number;
  name: string;
  bio?: string;
  avatarUrl?: string;
  social?: { type: string; url: string }[];
}

@Component({
  selector: 'app-speaker',
  templateUrl: './speaker.component.html',
  styleUrls: ['./speaker.component.scss']
})
export class SpeakerComponent {
  @Input() speakers: Speaker[] = [];
}