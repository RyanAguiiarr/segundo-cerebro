---
title: "TILA — Coding Conventions"
type: context
last_updated: 2026-06-09
---

# TILA — Coding Conventions
> Verified against real codebase on 2026-06-09

## Confirmed Conventions (verified in real files)

### Backend

| Convention | Verified in | Compliance |
|---|---|---|
| `ResponseEntity<GenericResult<T>>` for all endpoints | All 4 controllers | 100% |
| DTOs as Java records with Bean Validation | 11 of 13 DTOs | ~85% |
| Constructor injection (no `@Autowired` field) | All services, most controllers | ~95% |
| `@Transactional` on write operations | PacienteService, LaudoService | ~70% |
| `@Transactional(readOnly=true)` on reads | PacienteService (partial) | ~40% |
| BCryptPasswordEncoder for passwords | SecurityConfigurations | 100% |
| UUID for Usuario ID | Usuario entity | 100% |
| IDENTITY for other entity IDs | Medico, Paciente, Exame, Laudo, etc. | 100% |
| Enums as @Enumerated(STRING) | All enum fields | 100% |
| @PrePersist/@PreUpdate for timestamps | Laudo, ConhecimentoMedico | 100% (where used) |

### Frontend

| Convention | Verified in | Compliance |
|---|---|---|
| Standalone components (no NgModule) | All 15 components | 100% |
| Lazy loading via `loadComponent()` | All 10 page routes | 100% |
| `inject()` for DI | AppComponent, interceptor, guard | ~80% |
| Functional interceptor (HttpInterceptorFn) | auth.interceptor.ts | 100% |
| Functional guard | auth.guard.ts | 100% |
| Angular Signals (via AuthStore) | AppComponent, interceptor | ~60% |
| CSS vanilla (no frameworks) | All components | 100% |
| `withCredentials: true` for API calls | authInterceptor | 100% |

## Intended but Violated (documented conventions not always followed)

| Convention | Violation | File(s) |
|---|---|---|
| No `@Autowired` imports | Residual import in AutenticacaoController, PacienteController | Import exists but not used |
| `@Transactional(readOnly=true)` on all reads | LogAuditoriaService, PacienteService.buscarPorId | Missing annotation |
| Response DTOs for all endpoints | LogAuditoriaController returns entity directly | `List<LogAuditoria>` not DTO |
| No unused imports | `import java.awt.*` in SecurityFilter | Line 19 |
| Secrets via environment variables | JWT secret, DB password, Gemini API key | application.properties |
| `secure=true` on cookies | Cookie has `secure(false)` | AutenticacaoController |
