export interface Speaker {
    id: number;
    name: string;
    bio?: string;
    photoUrl?: string;
    events?: number[]; // Array of event IDs
  }