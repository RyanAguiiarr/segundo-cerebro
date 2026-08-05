---
title: "Spring Boot Backend — TILA"
type: entity
tags: [backend, spring-boot, java, tech-stack]
sources: [raw/codebase/snapshots/backend-structure.md]
last_updated: 2026-05-07
---

# Spring Boot Backend — TILA

## Stack Verificado
- **Java 21** — records, pattern matching, virtual threads
- **Spring Boot 4.0.3** — SecurityFilterChain, Spring Data JPA, Validation
- **PostgreSQL** — `localhost:5434/vectorDB` (migrado de TilaDB:5433)
- **Auth0 java-jwt 4.4.0** — geração/validação JWT com HMAC256
- **Lombok** — @Getter, @Setter, @NoArgsConstructor, @AllArgsConstructor
- **LangChain4j 0.36.2** — framework AI com Google Gemini + pgvector
- **Maven Wrapper** — build tool

## Entidades JPA (7)
| Entidade | Tabela | ID Type | Status |
|---|---|---|---|
| [[wiki/entities/entity-usuario]] | `usuarios` | UUID | ✅ Funcional |
| [[wiki/entities/entity-medico]] | `medicos` | Long | ✅ Funcional |
| [[wiki/entities/entity-paciente]] | `pacientes` | Long | ✅ Funcional |
| [[wiki/entities/entity-exame]] | `exames` | Long | ✅ Parcial |
| [[wiki/entities/entity-laudo]] | `laudo` (default) | Long | ✅ Criada (sem CRUD) |
| [[wiki/entities/entity-log-auditoria]] | `logs_auditoria` | Long | ✅ Parcial |
| [[wiki/entities/entity-conhecimento-medico]] | `conhecimento_medico` | Long | ✅ Criada (sem CRUD) |

## Camadas
- **Controllers**: AutenticacaoController, PacienteController, logAuditoriaController
- **Services**: PacienteService, AutenticacaoService, logAuditoriaService, TokenService, GenericResult
- **Repositories**: 7 repositórios (um por entidade)
- **AI Config**: TilaRagConfig — Gemini chat + embedding + pgvector store

## Observações Importantes
- ⚠️ DB mudou de `TilaDB:5433` para `vectorDB:5434` (para suportar pgvector)
- ⚠️ Entidades Laudo e ConhecimentoMedico existem mas sem controllers/services
- ⚠️ Consulta entity é placeholder vazio
- ⚠️ 3 secrets hardcoded em application.properties

## Backlinks
- [[wiki/concepts/data-model]]
- [[wiki/concepts/api-endpoints]]
- [[wiki/concepts/backend-services]]
- [[wiki/concepts/backend-patterns]]
- [[context/security-lgpd]]
