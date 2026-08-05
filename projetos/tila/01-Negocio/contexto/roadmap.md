---
title: "TILA — Roadmap"
type: context
last_updated: 2026-06-09
---

# TILA — Roadmap
> Derived from real gaps found in the 2026-06-09 audit.

## Phase 1 — Security hardening (NOW — before any staging deploy)
- [ ] Move JWT secret to `${JWT_SECRET}` environment variable
- [ ] Move DB password to `${DB_PASSWORD}` environment variable
- [ ] Remove hardcoded GEMINI_API_KEY from application.properties
- [ ] Set cookie `secure(true)` (production profile)
- [ ] Remove unused `import java.awt.*` from SecurityFilter
- [ ] Set `ddl-auto=validate` for production profile
- [ ] Set `show-sql=false` for production profile
- [ ] Add rate limiting to `/auth/login` and `/auth/registrar`
- [ ] Protect `/auth/registrar` with CRM verification or ADMIN approval
- [ ] Create LogAuditoriaResponseDTO — stop returning entity directly
- [ ] Capture `ipOrigem` (request.getRemoteAddr()) in all audit log entries

## Phase 2 — Feature completion (NEXT)
- [ ] Exame CRUD endpoints (POST, GET, PUT, DELETE)
- [ ] Laudo review endpoint (PUT /laudo/{id} with LaudoRevisaoRequestDTO)
- [ ] Laudo get endpoint (GET /laudo/{id})
- [ ] Logout endpoint (clear accessToken cookie)
- [ ] Consulta entity implementation (currently empty placeholder)
- [ ] Frontend: LaudoIaComponent — review/edit/sign workflow
- [ ] Frontend: CentroLaudosComponent — list and filter laudos
- [ ] Frontend: AgendaComponent — full implementation
- [ ] Frontend: Loading states for async operations
- [ ] Remove "s" dependency from package.json (likely typo)
- [ ] Add @Transactional(readOnly=true) to all read-only service methods

## Phase 3 — AI pipeline (FUTURE)
- [ ] Connect RAG to laudo generation flow (use TilaRadiologistaAgent instead of raw ChatModel)
- [ ] Build ingestão pipeline for ConhecimentoMedico → embeddings
- [ ] Implement RLHF: capture diff between rascunhoIA and textoFinal
- [ ] DICOM pipeline: DCM4CHE integration, tag parsing, metadata scrubbing
- [ ] Resolve model conflict: gemini-2.5-flash (bean) vs gemini-1.5-flash (properties)
- [ ] Expand beyond RX de Tórax to other modalities
- [ ] Add monitoring: latency, cost per call, confidence score metrics

## Phase 4 — Production readiness (FUTURE)
- [ ] LGPD full compliance: CPF encryption at rest, clinical data encryption
- [ ] Patient consent flow (opt-in for AI-assisted laudos)
- [ ] Right to erasure endpoint (anonimização)
- [ ] HTTPS everywhere (production CORS with real domain)
- [ ] Flyway migrations (replace ddl-auto=update)
- [ ] Observability: metrics, tracing, structured logging
- [ ] Backup strategy for PostgreSQL + pgvector
- [ ] CI/CD pipeline (GitLab CI already scaffolded)
