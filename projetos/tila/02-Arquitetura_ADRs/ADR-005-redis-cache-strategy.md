---
title: "ADR-005: Redis Caching Strategy"
type: decision
tags: [architecture, adr, redis, cache]
sources: [wiki/concepts/redis-cache-patterns.md]
last_updated: 2026-06-06
---

# ADR-005: Redis Caching Strategy

## Status
Accepted

## Context
A aplicação Tila necessita de alta performance e escalabilidade. Consultas complexas ao banco de dados relacional para resgatar prontuários de pacientes e exames podem introduzir latência desnecessária caso sejam requisitados repetidamente. Adicionalmente, chamadas à API da inteligência artificial (Gemini) são onerosas e devem ser controladas via rate-limiting para conter custos e abusos.

## Decision
Adotaremos o **Redis** como camada de cache em memória no backend da aplicação:
1. **Cache de Prontuários e Exames**: Salvar o JSON resultante no Redis com TTL curto (ex: 5 a 10 minutos) usando chaves prefixadas como `prontuario:{pacienteId}`.
2. **Session Store**: Salvar tokens expirados/invalidados ou sessões ativas com TTL igual ao de expiração do JWT.
3. **Rate Limiting**: Utilizar estruturas do Redis (counters) para bloquear abusos de requisições de geração de laudo por usuário (HTTP 429 se exceder o limite de requisições por minuto).

## Alternatives Considered

### Alternativa 1: Cache local em memória do Spring Boot (ex: Caffeine/Ehcache)
Rejeitada porque não escala horizontalmente caso tenhamos múltiplos containers do backend rodando. O Redis funciona de maneira distribuída e centralizada.

### Alternativa 2: Confiar apenas no cache do navegador (HTTP Cache)
Rejeitada porque não permite controle fino de invalidação, não protege contra chamadas maliciosas ou redundantes que forçam o bypass de cache no navegador, e não soluciona problemas como rate-limiting no servidor.

## Consequences

### Positivas
- Latência de leitura sub-milissegundo para dados quentes.
- Redução de carga no PostgreSQL.
- Controle centralizado de rate limit e sessões.

### Negativas
- Aumento de complexidade na infraestrutura (necessidade de manter o container do Redis ativo e gerenciar políticas de expiração e invalidação de cache).

### Riscos
- Inconsistência temporária de dados se o cache não for invalidado corretamente após uma atualização de prontuário (resolvido por eviction rules e TTL curto).

## Backlinks
- [[wiki/concepts/redis-cache-patterns]]
