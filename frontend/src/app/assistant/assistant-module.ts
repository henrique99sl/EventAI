import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { AssistantComponent } from './assistant.component';
import { AssistantChatComponent } from './assistant-chat/assistant-chat';
import { AssistantHistoryComponent } from './assistant-history/assistant-history';

@NgModule({
  declarations: [
    AssistantComponent,
    AssistantChatComponent,
    AssistantHistoryComponent
  ],
  imports: [
    CommonModule,
    FormsModule // <-- Adicionado para suportar ngModel!
  ],
  exports: [
    AssistantComponent,
    AssistantChatComponent,
    AssistantHistoryComponent
  ]
})
export class AssistantModule {}