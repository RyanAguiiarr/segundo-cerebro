---
title: "Angular Frontend — TILA"
type: entity
tags: [frontend, angular, tech-stack]
sources: []
last_updated: 2026-05-07
---

# Angular Frontend — TILA

## Stack Verificado
- **Angular 19.2.x** — Standalone components, Signals, functional guards/interceptors
- **TypeScript 5.7.2**
- **RxJS 7.8.x**
- **CSS Vanilla** — sem frameworks CSS
- **Inter (Google Fonts)** — tipografia
- **Port**: localhost:4200

## Componentes (14)
- 10 páginas: Login, Cadastro, Dashboard, Pacientes, CadastroPaciente, Prontuario, LaudoIA, CentroLaudos, Logs, Agenda
- 4 compartilhados: Header, Footer, Sidebar, SecurityBadges

## Services (6)
- 4 API services: AuthApi, PacienteApi, AgendaApi, LogAuditoria
- 2 stores: AuthStore (signal-based), MedicalStore (signal-based)

## Estado Atual
| Área | Status |
|---|---|
| Autenticação | ✅ Funcional (login, cadastro, guard) |
| Pacientes | ✅ Funcional (lista, cadastro, prontuário) |
| Logs | ✅ Funcional |
| Dashboard | ⚠️ Dados mockados |
| Laudo IA | ⚠️ Completamente mockado |
| Centro de Laudos | ⚠️ Completamente mockado |
| Agenda | ⚠️ Sem backend (mock local) |

## Referências
- [[wiki/concepts/frontend-architecture]] — Inventário completo
- [[wiki/concepts/angular-patterns]] — Padrões de código
- [[wiki/concepts/api-endpoints]] — Endpoints consumidos

## Backlinks
- [[wiki/overview]]
- [[wiki/entities/spring-boot-backend]]
