import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // <-- ADICIONADO!
import { LiveComponent } from './live.component';
import { LiveChatComponent } from './live-chat/live-chat';
import { VotingComponent } from './voting/voting';
import { StatsComponent } from './stats/stats';
import { UpdatesComponent } from './updates/updates';

@NgModule({
  declarations: [
    LiveComponent,
    LiveChatComponent,
    VotingComponent,
    StatsComponent,
    UpdatesComponent
  ],
  imports: [
    CommonModule,
    FormsModule // <-- ADICIONADO!
  ],
  exports: [LiveComponent]
})
export class LiveModule {}