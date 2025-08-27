export interface Event {
    id: number;
    title: string;
    description: string;
    date: string; // ISO date string
    location: string;
    speakers?: number[]; // Array of speaker IDs
    attendees?: number[]; // Array of user IDs
  }