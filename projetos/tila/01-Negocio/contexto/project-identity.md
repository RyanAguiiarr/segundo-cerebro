---
title: "TILA — Project Identity"
type: context
last_updated: 2026-06-09
---

# TILA — Project Identity

## Name
TILA — Tecnologia Integradora de Laudos Automatizados

## Team
- **Ryan Cantareli de Aguiar** — Full-stack developer, project lead
- **Pedro Henrique Oliveira Pereira** — Full-stack developer

## Repos (verified 2026-06-09)
| Repo | Path | Purpose |
|---|---|---|
| Tila_BackEnd | `c:\Tila\Tila_BackEnd` | Spring Boot 4 REST API + AI pipeline |
| Tila_Frontend | `c:\Tila\Tila_Frontend` | Angular 19 SPA |
| Tila_Brain | `c:\Tila\Tila_Brain` | Knowledge base (this repo) |

## Stack (exact versions from pom.xml and package.json)

### Backend
| Technology | Version |
|---|---|
| Java | 21 |
| Spring Boot | 4.0.3 |
| Spring Security | via Spring Boot parent |
| Spring Data JPA | via Spring Boot parent |
| Jackson | 3.x (Spring Boot 4 default) |
| LangChain4j BOM | 1.0.1 |
| auth0 java-jwt | 4.4.0 |
| PostgreSQL | runtime driver |
| pgvector | via langchain4j-pgvector |
| Lombok | 1.18.42 |
| Gemini model | gemini-2.5-flash (bean) / gemini-1.5-flash (properties) |
| Embedding model | gemini-embedding-001 (768 dims) |

### Frontend
| Technology | Version |
|---|---|
| Angular | 19.2.x |
| Angular CLI | 19.2.23 |
| TypeScript | 5.7.2 |
| RxJS | 7.8.x |
| zone.js | 0.15.x |
| Build tool | @angular-devkit/build-angular 19.2.23 |
| CSS | Vanilla (no framework) |
| Test | Karma 6.4 + Jasmine 5.6 |

### Infrastructure
| Component | Details |
|---|---|
| Database | PostgreSQL (vectorDB) at localhost:5434 |
| Vector DB | pgvector extension on same PostgreSQL |
| AI provider | Google Gemini via LangChain4j |
| Build | Maven (backend), npm/bun (frontend) |
| VCS | Git (GitLab) |

## Current implementation status (2026-06-09)

| Feature | Status | Notes |
|---|---|---|
| JWT authentication | ✅ Complete | HttpOnly cookie + header fallback |
| User registration | ✅ Complete | Médico only |
| Paciente CRUD | ✅ Complete | Create, list, get by id/cpf |
| Exame entity | ⚠️ Partial | Entity exists, no CRUD endpoints |
| Laudo generation (IA) | ✅ Functional | POST /laudo via Gemini |
| Laudo review/sign | ❌ Missing | LaudoRevisaoRequestDTO exists, no endpoint |
| Audit logging | ✅ Complete | LogAuditoria entity + controller |
| Angular pages | ✅ 10 pages | login, cadastro, dashboard, pacientes, prontuario, laudo-ia, centro-laudos, logs, agenda |
| DICOM pipeline | ❌ Not started | No DICOM code in project |
| RAG pipeline | ⚠️ Configured | pgvector + embeddings configured, not connected to flow |
| RLHF feedback | ❌ Not started | No feedback capture |
