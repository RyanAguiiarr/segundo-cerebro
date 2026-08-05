---
title: "Estado local de componentes TILA usa Angular Signals — Subject/BehaviorSubject só para streams"
type: pattern
domain: frontend
tags: [angular, signals, state]
verified_in: [AppComponent (inject(AuthStore)), auth.interceptor.ts (inject(AuthStore))]
violations_found: []
last_updated: 2026-06-09
---

# Estado local de componentes TILA usa Angular Signals — Subject/BehaviorSubject só para streams

## O padrão

O TILA adota Angular Signals (Angular 19) para gerenciamento de estado. O `AuthStore` é um service baseado em Signals que gerencia o estado de autenticação globalmente.

## Verificado no código

### AppComponent
```typescript
private authStore = inject(AuthStore);
// Chama authStore.fetchProfile() no ngOnInit
```

### authInterceptor
```typescript
const authStore = inject(AuthStore);
// Chama authStore.logout() em erro 401/403
```

### Padrão inject() em vez de constructor
```typescript
// ✅ Padrão TILA
private router = inject(Router);
private authStore = inject(AuthStore);
```

## Conformidade: ~60-80%
- AuthStore usa Signals ✅
- AppComponent usa inject() ✅
- Functional interceptor e guard usam inject() ✅
- Componentes de página precisam verificação individual

## RxJS ainda presente
- `filter()` e `subscribe()` em AppComponent para NavigationEnd
- `catchError()` e `throwError()` no interceptor
- ✅ Uso justificado: streams de eventos do Router são RxJS por natureza

## Backlinks
- [[negocio/permanent/decisoes/ADR-007-angular-signals-state-management]]
- [[codebase/snapshots/frontend-audit-2026-06-09]]
