import { Component, Input } from '@angular/core';

export interface SpeakerItem {
  id: number;
  name: string;
  bio?: string;
  avatarUrl?: string;
  topics?: string[];
  social?: { type: string; url: string }[];
}

@Component({
  selector: 'app-speaker-list',
  templateUrl: './speaker-list.html',
  styleUrls: ['./speaker-list.scss']
})
export class SpeakerListComponent {
  @Input() speakers: SpeakerItem[] = [];
}