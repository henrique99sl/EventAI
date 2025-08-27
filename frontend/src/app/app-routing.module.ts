import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainLayoutComponent } from './main-layout/main-layout.component'; // Certifica-te que este componente existe

const routes: Routes = [
  // Landing page sem layout
  { path: '', loadChildren: () => import('./landing/landing-module').then(m => m.LandingModule) },

  // Todas as páginas principais com layout
  {
    path: '',
    component: MainLayoutComponent,
    children: [
      { path: 'auth', loadChildren: () => import('./auth/auth-module').then(m => m.AuthModule) },
      { path: 'dashboard', loadChildren: () => import('./dashboard/dashboard-module').then(m => m.DashboardModule) },
      { path: 'agenda', loadChildren: () => import('./agenda/agenda-module').then(m => m.AgendaModule) },
      { path: 'speaker', loadChildren: () => import('./speaker/speaker-module').then(m => m.SpeakerModule) },
      { path: 'live', loadChildren: () => import('./live/live-module').then(m => m.LiveModule) },
      { path: 'feedback', loadChildren: () => import('./feedback/feedback-module').then(m => m.FeedbackModule) },
      { path: 'organizer', loadChildren: () => import('./organizer/organizer-module').then(m => m.OrganizerModule) },
      { path: 'assistant', loadChildren: () => import('./assistant/assistant-module').then(m => m.AssistantModule) },
    ]
  },

  // Not Found (404)
  { path: '**', loadChildren: () => import('./not-found/not-found-module').then(m => m.NotFoundModule) }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}