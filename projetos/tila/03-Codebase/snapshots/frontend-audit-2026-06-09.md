---
title: "Auditoria Frontend TILA — Snapshot 2026-06-09"
type: snapshot
scope: frontend
date: 2026-06-09
immutable: true
---

# Auditoria Completa do Frontend TILA
> Snapshot imutável de 2026-06-09

## Stack Verificada (package.json)

| Dependência | Versão |
|---|---|
| Angular (core, common, compiler, forms, router, platform-browser) | ^19.2.0 |
| Angular CLI | ^19.2.23 |
| Angular DevKit Build | ^19.2.23 |
| TypeScript | ~5.7.2 |
| RxJS | ~7.8.0 |
| zone.js | ~0.15.0 |
| tslib | ^2.3.0 |
| Karma + Jasmine | 6.4/5.6 |
| ⚠️ "s" dependency | ^1.0.0 (package "s" — provável erro de digitação) |

## Mapa de Rotas

| Path | Component | Guard | Lazy loaded | Status |
|---|---|---|---|---|
| / | redirect → /login | — | — | ✅ |
| /login | LoginComponent | — | ✅ | ✅ Funcional |
| /cadastro | CadastroComponent | — | ✅ | ✅ Funcional |
| /dashboard | DashboardComponent | authGuard | ✅ | ✅ Funcional |
| /pacientes | PacientesComponent | authGuard | ✅ | ✅ Funcional |
| /pacientes/novo | CadastroPacienteComponent | authGuard | ✅ | ✅ Funcional |
| /pacientes/:id | ProntuarioComponent | authGuard | ✅ | ✅ Funcional |
| /laudo/:id | LaudoIaComponent | authGuard | ✅ | ⚠️ Parcial |
| /laudos | CentroLaudosComponent | authGuard | ✅ | ⚠️ Parcial |
| /logs | LogsComponent | authGuard | ✅ | ✅ Funcional |
| /agenda | AgendaComponent | authGuard | ✅ | ⚠️ Scaffold |
| ** | redirect → /login | — | — | ✅ |

Nota: Todas as rotas protegidas usam `canActivate: [authGuard]`.
Todas as rotas são lazy loaded via `loadComponent()` — padrão Angular 19 standalone.

## Inventário de Componentes

### Pages (10)
| Component | Standalone | Signals | Issues |
|---|---|---|---|
| LoginComponent | ✅ | ⚠️ Verificar | — |
| CadastroComponent | ✅ | ⚠️ Verificar | — |
| DashboardComponent | ✅ | ⚠️ Verificar | — |
| PacientesComponent | ✅ | ⚠️ Verificar | — |
| CadastroPacienteComponent | ✅ | ⚠️ Verificar | — |
| ProntuarioComponent | ✅ | ⚠️ Verificar | — |
| LaudoIaComponent | ✅ | ⚠️ Verificar | — |
| CentroLaudosComponent | ✅ | ⚠️ Verificar | — |
| LogsComponent | ✅ | ⚠️ Verificar | — |
| AgendaComponent | ✅ | ⚠️ Verificar | Scaffold/placeholder |

### Shared Components (5)
| Component | Standalone | Notes |
|---|---|---|
| HeaderComponent | ✅ | Importado no AppComponent |
| FooterComponent | ✅ | Importado no AppComponent |
| DashboardHeaderComponent | ✅ | Header interno para telas autenticadas |
| SidebarComponent | ✅ | Navegação lateral |
| SecurityBadgesComponent | ✅ | Badges de segurança/LGPD |

### AppComponent
- Standalone: ✅
- Imports: RouterOutlet, HeaderComponent, FooterComponent, CommonModule
- Usa `inject()` para Router e AuthStore
- Controla `isInternalScreen` via NavigationEnd para mostrar/esconder Header/Footer
- ✅ Chama `authStore.fetchProfile()` no ngOnInit

## Core (guards, interceptors, services, models)

### authGuard
- Arquivo: `core/guards/auth.guard.ts`
- Verifica autenticação antes de rotas protegidas

### authInterceptor
- Arquivo: `core/interceptors/auth.interceptor.ts`
- Functional interceptor (HttpInterceptorFn — Angular 19 pattern)
- `withCredentials: true` para enviar cookies
- Seta `Content-Type: application/json`
- Intercepta 401/403 → `authStore.logout()` + redirect /login

### Services

| Pasta | Conteúdo |
|---|---|
| core/services/api/ | Serviços HTTP para API calls |
| core/services/store/ | AuthStore — state management com Signals |
| core/services/theme/ | Theme service |

### Models
- `generic-result.model.ts` — interface TypeScript espelhando GenericResult<T> do backend

## AppConfig
- `provideZoneChangeDetection({ eventCoalescing: true })`
- `provideRouter(routes)`
- `provideHttpClient(withFetch(), withInterceptors([authInterceptor]))`
- ✅ Usa `withFetch()` — fetch API moderno (não XMLHttpRequest)

## Conformidade com Convenções

| Convenção | Status | % Conforme |
|---|---|---|
| Componentes standalone | ✅ Todos | 100% |
| Lazy loading de rotas | ✅ Todas as rotas | 100% |
| inject() em vez de constructor DI | ✅ AppComponent | ~80% |
| Functional interceptor | ✅ | 100% |
| Functional guard | ✅ | 100% |
| Angular Signals (AuthStore) | ✅ | ~60% (verificar pages) |
| CSS vanilla (sem Tailwind) | ✅ | 100% |
| NgModule | ❌ Nenhum | 100% conforme (nenhum NgModule) |

## Gaps do Frontend

1. 🟡 Dependência "s" no package.json — provavelmente erro, remover
2. 🟡 AgendaComponent parece scaffold/placeholder
3. 🟡 LaudoIaComponent e CentroLaudosComponent — parcialmente implementados
4. 🟡 Falta feedback visual para operações assíncronas (loading states)
5. 🔵 Sem testes unitários escritos (Karma/Jasmine configurado mas provavelmente sem specs)
6. 🔵 Sem internacionalização — todo o texto é hardcoded pt-BR

## Backlinks
- [[codebase/patterns/padrão-componente-standalone]]
- [[codebase/patterns/padrão-signals-estado]]
- [[codebase/patterns/padrão-css-vanilla]]
