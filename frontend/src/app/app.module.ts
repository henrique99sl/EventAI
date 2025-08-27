import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppComponent } from './app';
import { AppRoutingModule } from './app-routing.module';

// Shared and Core modules (globais, reutilizáveis)
import { SharedModule } from './shared/shared.module';
import { CoreModule } from './core/core.module';

// Angular Material centralizado
import { MaterialModule } from './shared/material/material.module';

// Importa o módulo do assistente, NÃO o componente!
// O caminho pode ser diferente, ajuste conforme sua estrutura.
import { AssistantModule } from './assistant/assistant-module';

// Exemplos de componentes globais (navbar, footer), descomenta/edita conforme existam
// import { NavbarComponent } from './shared/components/navbar/navbar.ts';
// import { FooterComponent } from './shared/components/footer/footer.ts';

// Não importes feature modules (como LiveModule, SpeakerModule) se estiverem lazy loaded via AppRoutingModule!
// Se algum módulo precisar ser carregado diretamente (eager), importa aqui.

@NgModule({
  declarations: [
    AppComponent,
    // NÃO inclui AssistantComponent aqui!
    // NavbarComponent,
    // FooterComponent,
    // Outros componentes globais - coloca aqui se existirem
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule, // Útil para formulários mais avançados
    HttpClientModule,
    AppRoutingModule,
    SharedModule,        // Pipes, diretivas e componentes reutilizáveis
    CoreModule,          // Serviços globais, guards, interceptors
    MaterialModule,      // Angular Material customizado
    AssistantModule,     // <-- Adicione aqui!
    // LiveModule,        // Só se NÃO estiver lazy loaded via routing
    // SpeakerModule,     // Só se NÃO estiver lazy loaded via routing
    // Outros módulos globais
  ],
  providers: [
    // Exemplo para adicionar interceptors globais:
    // {
    //   provide: HTTP_INTERCEPTORS,
    //   useClass: AuthInterceptor,
    //   multi: true
    // }
    // Outros serviços globais, guards, etc. (preferencialmente em CoreModule)
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}