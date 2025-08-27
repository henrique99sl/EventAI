import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { OrganizerComponent } from './organizer.component';
import { MetricsComponent } from './metrics/metrics';
import { ExportReportsComponent } from './export-reports/export-reports';
import { NotificationsAdminComponent } from './notifications-admin/notifications-admin';
import { EditEventComponent } from './edit-event/edit-event';

@NgModule({
  declarations: [
    OrganizerComponent,
    MetricsComponent,
    ExportReportsComponent,
    NotificationsAdminComponent,
    EditEventComponent
  ],
  imports: [
    CommonModule,
    FormsModule
  ],
  exports: [
    OrganizerComponent,
    MetricsComponent,
    ExportReportsComponent,
    NotificationsAdminComponent,
    EditEventComponent
  ]
})
export class OrganizerModule {}