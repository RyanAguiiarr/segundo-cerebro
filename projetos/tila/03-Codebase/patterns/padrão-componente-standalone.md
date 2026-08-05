---
title: "Todos os componentes Angular do TILA são standalone — NgModule é proibido"
type: pattern
domain: frontend
tags: [angular, standalone, components]
verified_in: [AppComponent, LoginComponent, CadastroComponent, DashboardComponent, PacientesComponent, CadastroPacienteComponent, ProntuarioComponent, LaudoIaComponent, CentroLaudosComponent, LogsComponent, AgendaComponent, HeaderComponent, FooterComponent, DashboardHeaderComponent, SidebarComponent, SecurityBadgesComponent]
violations_found: []
last_updated: 2026-06-09
---

# Todos os componentes Angular do TILA são standalone — NgModule é proibido

## O padrão

O TILA usa exclusivamente standalone components (Angular 19). Nenhum `NgModule` existe no projeto. Imports são declarados diretamente no decorator `@Component`.

## Exemplo real (verificado — AppComponent)

```typescript
@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HeaderComponent, FooterComponent, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit { ... }
```

## Routing usa loadComponent (não loadChildren com module)

```typescript
{ path: 'login', loadComponent: () => import('./pages/login/login.component').then(m => m.LoginComponent) }
```

Todas as 10 rotas de páginas usam `loadComponent()` com lazy loading.

## Conformidade: 100%
- 15 componentes verificados — todos standalone
- 0 NgModules no projeto
- AppConfig usa `provideRouter` em vez de `RouterModule.forRoot`

## Backlinks
- [[negocio/permanent/decisoes/ADR-004-angular-standalone-sem-ngmodule]]
- [[codebase/snapshots/frontend-audit-2026-06-09]]
