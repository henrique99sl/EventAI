import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MainLayoutComponent } from './main-layout.component';
import { RouterModule } from '@angular/router';
import { AssistantModule } from '../assistant/assistant-module';

@NgModule({
  declarations: [MainLayoutComponent],
  imports: [
    CommonModule,
    RouterModule,
    AssistantModule
  ],
  exports: [MainLayoutComponent]
})
export class MainLayoutModule {}