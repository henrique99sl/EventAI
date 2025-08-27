import { NgModule, Optional, SkipSelf, ErrorHandler } from '@angular/core';

// Import and provide global services here
// import { ApiService } from './core/api/api';
// import { AuthService } from './core/auth/auth';
// import { WebsocketService } from './core/websocket/websocket';
// import { GlobalErrorHandler } from './core/error/error-handler';
// import { ToastService } from './core/error/toast.service';

@NgModule({
  providers: [
    // ApiService,
    // AuthService,
    // WebsocketService,
    // { provide: ErrorHandler, useClass: GlobalErrorHandler },
    // ToastService,
    // ... add other global services
  ]
})
export class CoreModule {
  constructor(@Optional() @SkipSelf() parentModule: CoreModule) {
    if (parentModule) {
      throw new Error('CoreModule has already been loaded. Import only in AppModule.');
    }
  }
}