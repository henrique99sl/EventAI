import { Component, Input, Output, EventEmitter } from '@angular/core';

export interface EventData {
  id: number;
  title: string;
  date: string;
  location: string;
  description: string;
}

@Component({
  selector: 'app-edit-event',
  templateUrl: './edit-event.html',
  styleUrls: ['./edit-event.scss']
})
export class EditEventComponent {
  @Input() event: EventData = {
    id: 0,
    title: '',
    date: '',
    location: '',
    description: ''
  };

  @Output() saveEvent = new EventEmitter<EventData>();
  @Output() cancelEdit = new EventEmitter<void>();

  onSave() {
    this.saveEvent.emit({ ...this.event });
  }

  onCancel() {
    this.cancelEdit.emit();
  }
}