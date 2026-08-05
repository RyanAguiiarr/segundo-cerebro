# Backend Structure Snapshot — 2026-05-07

## Core Versions
- **Java**: 21
- **Spring Boot**: 4.0.3
- **Maven Wrapper**: bundled

## Dependencies

| Dependency | Version | Purpose |
|---|---|---|
| spring-boot-starter-data-jpa | via Boot 4.0.3 | ORM / JPA / Hibernate |
| spring-boot-starter-security | via Boot 4.0.3 | Authentication / Authorization |
| spring-boot-starter-security-oauth2-authorization-server | via Boot 4.0.3 | OAuth2 server support (NOT actively used) |
| spring-boot-starter-validation | via Boot 4.0.3 | Bean Validation (Jakarta) |
| spring-boot-starter-webmvc | via Boot 4.0.3 | REST controllers |
| spring-boot-devtools | via Boot 4.0.3 | Hot reload (runtime, optional) |
| postgresql | runtime | PostgreSQL JDBC driver |
| lombok | latest (optional) | Boilerplate reduction (@Getter, @Setter, etc.) |
| auth0/java-jwt | 4.4.0 | JWT generation and validation |
| langchain4j (BOM) | 0.36.2 | AI framework - core |
| langchain4j-spring-boot-starter | via BOM | Spring Boot auto-config for LC4J |
| langchain4j-google-ai-gemini | via BOM | Google Gemini chat + embedding models |
| langchain4j-pgvector | via BOM | PgVector embedding store |

## Package Map

| Package | Responsibility |
|---|---|
| `tecnologi.tila.tila` | Root — TilaApplication entry point |
| `tecnologi.tila.tila.ai.config` | AI/RAG configuration (TilaRagConfig) |
| `tecnologi.tila.tila.config` | Security config (SecurityConfigurations, SecurityFilter) |
| `tecnologi.tila.tila.controller` | REST controllers (Auth, Paciente, LogAuditoria) |
| `tecnologi.tila.tila.dto` | Data Transfer Objects (records) |
| `tecnologi.tila.tila.entity` | JPA entities (7 entities) |
| `tecnologi.tila.tila.enuns` | Enums (PerfilUser, StatuExame, StatusLaudo, etc.) |
| `tecnologi.tila.tila.exceptions` | Global exception handler |
| `tecnologi.tila.tila.repository` | Spring Data JPA repositories |
| `tecnologi.tila.tila.service` | Business logic + GenericResult |
| `tecnologi.tila.tila.service.athenticate` | Auth service (⚠️ TYPO in package name) |
| `tecnologi.tila.tila.service.paciente` | Paciente service |
| `tecnologi.tila.tila.service.logAuditoria` | Log auditoria service |

## Configuration Summary

- **DB URL**: `jdbc:postgresql://localhost:5434/vectorDB`
- **DB Driver**: org.postgresql.Driver
- **DDL Auto**: `update` (⚠️ dangerous for production)
- **JPA Dialect**: PostgreSQLDialect
- **Show SQL**: true
- **Server Port**: 8080 (default)
- **Upload Path**: `./uploads/exames`
- **Upload Max Size**: 50MB
- **Gemini Model (chat)**: gemini-1.5-flash (config) / gemini-2.5-flash (code)
- **Gemini Model (embedding)**: text-embedding-004
- **Gemini Temperature**: 0.3
- **Gemini Max Output Tokens**: 4096

## ⚠️ SECURITY GAPS FOUND

1. ⚠️ **JWT secret hardcoded**: `api.security.token.secret="Cucamole@123"` in application.properties
2. ⚠️ **DB password hardcoded**: `spring.datasource.password=Cucamole@123` in application.properties
3. ⚠️ **Gemini API key hardcoded**: `GEMINI_API_KEY=AIzaSy...` directly in application.properties (even though `${GEMINI_API_KEY}` is also configured above)
4. ⚠️ **DB changed from SKILL.md**: Was `TilaDB:5433`, now `vectorDB:5434` — likely a second DB for pgvector

## Divergences from Previous SKILL.md
- SKILL.md listed DB as `localhost:5433/TilaDB` → actual is `localhost:5434/vectorDB`
- SKILL.md did not document LangChain4j, pgvector, or AI config
- SKILL.md said Laudo entity "does not exist" → it NOW EXISTS
- New entity `ConhecimentoMedico` not in SKILL.md
- New enum `CategoriaConhecimento` not in SKILL.md
- New enum `StatusLaudo` not in SKILL.md
- New package `ai.config` with `TilaRagConfig` not in SKILL.md
- `spring-boot-starter-security-oauth2-authorization-server` dependency not in SKILL.md
