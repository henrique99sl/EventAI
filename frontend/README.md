# EventAI Frontend

Bem-vindo ao **EventAI Frontend**!  
Este projeto é uma aplicação web moderna desenvolvida em **Angular** (standalone components e modules), utilizando **Angular Material**, com arquitetura modular, testes automatizados e integração com backend via serviços REST.  
Abaixo tens uma documentação detalhada para desenvolvedores, mantenedores e novos colaboradores.

---

## Índice

- [Visão Geral](#visão-geral)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Instalação e Configuração](#instalação-e-configuração)
- [Scripts NPM](#scripts-npm)
- [Configuração Angular](#configuração-angular)
- [Como Executar](#como-executar)
- [Testes](#testes)
- [Principais Módulos e Funcionalidades](#principais-módulos-e-funcionalidades)
- [Estilos e Temas](#estilos-e-temas)
- [Internacionalização (i18n)](#internacionalização-i18n)
- [Como criar novos componentes/módulos](#como-criar-novos-componentesmódulos)
- [Boas práticas de desenvolvimento](#boas-práticas-de-desenvolvimento)
- [Resolução de problemas comuns](#resolução-de-problemas-comuns)
- [Licença](#licença)

---

## Visão Geral

Esta aplicação permite organizar, gerir e interagir com eventos, incluindo funcionalidades para agenda, feedback, sessões ao vivo, assistente de IA, autenticação, dashboards, perfis de oradores e organizadores, entre outros.

- **Framework:** Angular 16+
- **Componentização:** Standalone components e modules
- **UI:** Angular Material
- **Testes:** Jasmine + Karma
- **Estilos:** SCSS modular + temas pré-definidos
- **Internacionalização:** Arquivos JSON em `src/assets/i18n/`
- **Arquitetura:** Modular, escalável, fácil de manter

---

## Estrutura de Pastas

```
src/
│
├── app/          # Tudo do frontend Angular
│   ├── agenda/           # Módulo de agenda de eventos
│   ├── assistant/        # Módulo de assistente IA (chat, histórico)
│   ├── auth/             # Autenticação: login, registo, recuperação
│   ├── core/             # Serviços de API, autenticação, modelos, utilidades
│   ├── dashboard/        # Dashboard principal e widgets
│   ├── feedback/         # Feedback de utilizadores e relatórios
│   ├── landing/          # Página inicial / landing page
│   ├── live/             # Sessões ao vivo e chat
│   ├── main-layout/      # Layout principal (navbar, footer, router-outlet)
│   ├── not-found/        # Página 404
│   ├── organizer/        # Funcionalidades do organizador
│   ├── shared/           # Componentes e pipes partilhados, material.module.ts
│   ├── speaker/          # Funcionalidades de oradores
│   ├── app-routing.module.ts  # Rotas principais
│   ├── app.module.ts         # Módulo principal
│   ├── app.config.ts         # Configuração global Angular
│   ├── app.ts                # Componente principal (AppComponent)
│   ├── app.html              # Template principal
│   ├── app.scss              # Estilos globais
│   ├── app.spec.ts           # Testes ao AppComponent
│
├── assets/
│   ├── fonts/
│   ├── i18n/         # Traduções em JSON (ex: pt.json, en.json)
│   ├── images/
│   └── styles/       # SCSS globais, variáveis, mixins, tema
│
├── environments/
│   ├── environment.ts
│   └── environment.prod.ts
│
├── index.html
├── main.ts
├── styles.scss        # Importa temas e estilos globais
```

---

## Instalação e Configuração

1. **Pré-requisitos:**
   - Node.js >= 18.x
   - npm >= 9.x
   - Angular CLI (`npm i -g @angular/cli`)

2. **Instalação:**
   ```sh
   npm install
   ```

3. **Configuração opcional:**
   - Verifica as variáveis de ambiente em `src/environments/`
   - Adapta o backend/API baseUrl em `environment.ts` conforme necessário

---

## Scripts NPM

- `npm start` ou `ng serve` — inicia ambiente de desenvolvimento
- `ng build` — compila para produção
- `ng test` — executa testes unitários (Karma/Jasmine)
- `ng lint` — verifica padrões e boas práticas
- `ng e2e` — testes end-to-end (se configurados)

---

## Configuração Angular

- **Angular.json:** Configura caminhos, build, assets, estilos globais.
- **tsconfig.json:** Configurações de TypeScript.
- **tsconfig.app.json / tsconfig.spec.json:** Configurações específicas para app e testes.
- **assets/styles:** Variáveis, mixins e tema SCSS importados em `styles.scss` e componentes.

---

## Como Executar

1. **Desenvolvimento:**
   ```sh
   npm start
   ```
   Acede a [http://localhost:4200](http://localhost:4200)

2. **Build para produção:**
   ```sh
   ng build --configuration production
   ```

3. **Testes:**
   ```sh
   ng test
   ```

---

## Testes

- **Unitários:** Jasmine/Karma, todos os componentes e serviços críticos têm testes em `.spec.ts`.
- **Cobertura:** Verifica relatório após testes, adiciona/ajusta testes para manter cobertura.

---

## Principais Módulos e Funcionalidades

- **Agenda:** Visualização e gestão de eventos, calendário, filtros.
- **Assistant:** Chat IA, histórico de conversas, integração potencial com backend de IA.
- **Auth:** Login, registo, recuperação/alteração de palavra-passe, social login.
- **Dashboard:** Painéis de controlo, widgets de notificações, feedback, assistência.
- **Feedback:** Formulários, relatórios, feedback gamificado.
- **Live:** Chat ao vivo, estatísticas, votações.
- **Organizer:** Gestão de eventos, relatórios, métricas, notificações administrativas.
- **Shared:** Componentes reutilizáveis (botão, cartão, input, loader, modal), pipes, material module.
- **Main Layout:** Layout global da app (navbar, router-outlet, footer).
- **Speaker:** Perfis, recomendações, lista de oradores.
- **Landing:** Página inicial, introdução ao produto/evento.
- **Not Found:** Página de erro 404.

---

## Estilos e Temas

- **Angular Material:** Tema importado em SCSS (`indigo-pink`, outros disponíveis).
- **Customização:** Variáveis, mixins e tema próprios em `src/assets/styles/`.
- **Responsividade:** SCSS mobile-first, media queries e layouts flex/grid.

---

## Internacionalização (i18n)

- Traduções em JSON (`src/assets/i18n/en.json`, `pt.json`, ...)
- Seleção de idioma via serviço Angular (customizável)
- Componentes e templates preparados para multi-idioma

---

## Como criar novos componentes/módulos

1. **Componente Standalone:**
   ```sh
   ng generate component my-component --standalone
   ```
2. **Módulo Novo:**
   ```sh
   ng generate module my-module
   ```
3. **Testes:**
   - Gera automaticamente `.spec.ts`
   - Mantém cobertura mínima e boas práticas

---

## Boas práticas de desenvolvimento

- **Organização Modular:** Cada funcionalidade no seu módulo/pasta.
- **Reutilização:** Usa componentes e serviços partilhados.
- **Testes:** Não faças merge sem testes adequados.
- **Estilos:** Prefere SCSS modular, importa variáveis/globals via `styles.scss`.
- **Commits:** Mensagens claras, uso de branches para features/bugs.
- **Pull Requests:** Sempre com descrição clara e referência a issues (quando possível).
- **Documentação:** Mantém este README e docs internos atualizados.

---

## Resolução de problemas comuns

- **Erro de import/export:** Verifica se o ficheiro exporta o componente/classe corretamente.
- **Problemas de SCSS:** Confirma o caminho dos imports e que os ficheiros existem.
- **Falha nos testes:** Garante que todos os inputs esperados nos testes existem no componente.
- **404 Not Found:** Verifica as rotas no `app-routing.module.ts` e os lazy modules.
- **Problemas de build:** Verifica dependências no `package.json` e Angular CLI version.

---

## Licença

Este projeto é open-source, disponível sob a licença MIT.  
Consulta o ficheiro `LICENSE` para detalhes.

---

## Dúvidas?

Abre uma **issue** ou entra em contacto com o mantenedor principal.
