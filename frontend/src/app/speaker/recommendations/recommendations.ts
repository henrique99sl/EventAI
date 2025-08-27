import { Component, Input } from '@angular/core';

export interface SpeakerRecommendation {
  id: number;
  name: string;
  bio?: string;
  avatarUrl?: string;
  topics?: string[];
  reason?: string;
}

@Component({
  selector: 'app-speaker-recommendations',
  templateUrl: './recommendations.html',
  styleUrls: ['./recommendations.scss']
})
export class SpeakerRecommendationsComponent {
  @Input() recommendations: SpeakerRecommendation[] = [];
}